from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import re

from copy import deepcopy
from dateutil.parser import parse
from collections import OrderedDict, namedtuple
from datetime import timedelta, datetime, date
import logging


from pydruid.utils.filters import Dimension, Filter
from pydruid.utils.having import Aggregation
from pydruid.utils.postaggregator import Postaggregator



from app.models.basemodel import db, get_session
from app.models.basemodel import BaseModel
from app.models.queryable import Queryable
from app.models.druid_column import *
from six import string_types
from app.utils import utils
from app.utils.utils import DimSelector

DTTM_ALIAS = '__timestamp'
QueryResult = namedtuple('namedtuple', ['df', 'query', 'duration'])


class JavascriptPostAggregator(Postaggregator):
    def __init__(self, name, field_names, function):
        self.post_aggregator = {
            'type': 'javascript',
            'fieldNames': field_names,
            'name': name,
            'function': function,
        }
        self.name = name


class DruidDatasource(BaseModel, Queryable):

    """ORM object referencing Druid datasources (tables)"""

    type = "druid"

    __tablename__ = 'druid_datasources'
    datasource_name = Column(String(255), unique=True)
    ekryp_partner_id = Column(Integer, ForeignKey("ekryp_partner.id"))
    description = Column(Text)
    default_endpoint = Column(Text)
    cluster = relationship('DruidCluster', backref=backref("datasources", cascade="all"))
    cluster_name = Column(String(250), ForeignKey('druid_clusters.cluster_name'))
    offset = Column(Integer, default=0)
    cache_timeout = Column(Integer)
    perm = Column(String(1000))
    columns = relationship("DruidColumn", backref=backref("columns", cascade="all"), lazy="dynamic")
    metrics = relationship("DruidMetric", backref=backref("metrics", cascade="all"), lazy="dynamic")

    def __init__(self, **kwargs):
        super(DruidDatasource, self).__init__(**kwargs)

    def __setitem__(self, key, value):
        self.key = value


    @property
    def database(self):
        return self.cluster

    @property
    def metrics_combo(self):
        return sorted(
            [(m.metric_name, m.verbose_name) for m in self.metrics],
            key=lambda x: x[1])

    @property
    def num_cols(self):
        return [c.column_name for c in self.columns if c.isnum]

    @property
    def name(self):
        return self.datasource_name

    @property
    def schema(self):
        name_pieces = self.datasource_name.split('.')
        if len(name_pieces) > 1:
            return name_pieces[0]
        else:
            return None



    @property
    def time_column_grains(self):
        return {
            "time_columns": [
                'all', '5 seconds', '30 seconds', '1 minute',
                '5 minutes', '1 hour', '6 hour', '1 day', '7 days',
                'week', 'week_starting_sunday', 'week_ending_saturday',
                'month','year', 'quarter','day'
            ],
            "time_grains": ['now']
        }

    def __repr__(self):
        return self.datasource_name

    def get_metric_obj(self, metric_name):
        return [
            m.json_obj for m in self.metrics
            if m.metric_name == metric_name
        ][0]

    @staticmethod
    def version_higher(v1, v2):
        """is v1 higher than v2

        >>> DruidDatasource.version_higher('0.8.2', '0.9.1')
        False
        >>> DruidDatasource.version_higher('0.8.2', '0.6.1')
        True
        >>> DruidDatasource.version_higher('0.8.2', '0.8.2')
        False
        >>> DruidDatasource.version_higher('0.8.2', '0.9.BETA')
        False
        >>> DruidDatasource.version_higher('0.8.2', '0.9')
        False
        """
        def int_or_0(v):
            try:
                v = int(v)
            except (TypeError, ValueError):
                v = 0
            return v
        v1nums = [int_or_0(n) for n in v1.split('.')]
        v2nums = [int_or_0(n) for n in v2.split('.')]
        v1nums = (v1nums + [0, 0, 0])[:3]
        v2nums = (v2nums + [0, 0, 0])[:3]
        return v1nums[0] > v2nums[0] or \
            (v1nums[0] == v2nums[0] and v1nums[1] > v2nums[1]) or \
            (v1nums[0] == v2nums[0] and v1nums[1] == v2nums[1] and v1nums[2] > v2nums[2])

    def latest_metadata(self):
        """Returns segment metadata from the latest segment"""
        client = self.cluster.get_pydruid_client()
        results = client.time_boundary(datasource=self.datasource_name)
        if not results:
            return
        max_time = results[0]['result']['maxTime']
        min_time = results[0]['result']['minTime']
        max_time = parse(max_time)
        min_time = parse(min_time)
        # Query segmentMetadata for 7 days back. However, due to a bug,
        # we need to set this interval to more than 1 day ago to exclude
        # realtime segments, which trigged a bug (fixed in druid 0.8.2).
        # https://groups.google.com/forum/#!topic/druid-user/gVCqqspHqOQ
        # lbound = (max_time - timedelta(days=7)).isoformat()
        lbound = min_time.isoformat() # set as min time because few columns are missing in some segments
        rbound = max_time.isoformat()
        if not self.version_higher(self.cluster.druid_version, '0.8.2'):
            rbound = (max_time - timedelta(1)).isoformat()
        segment_metadata = None
        try:
            segment_metadata = client.segment_metadata(
                datasource=self.datasource_name,
                intervals=lbound + '/' + rbound)
        except Exception as e:
            logging.warning("Failed first attempt to get latest segment")
            logging.exception(e)
        if not segment_metadata:
            # if no segments in the past 7 days, look at all segments
            lbound = datetime(1901, 1, 1).isoformat()[:10]
            rbound = datetime(2050, 1, 1).isoformat()[:10]
            if not self.version_higher(self.cluster.druid_version, '0.8.2'):
                rbound = datetime.now().isoformat()[:10]
            try:
                segment_metadata = client.segment_metadata(
                    datasource=self.datasource_name,
                    intervals=lbound + '/' + rbound)
            except Exception as e:
                logging.warning("Failed 2nd attempt to get latest segment")
                logging.exception(e)
        # return segment_metadata[-1]["columns"]
        final_segment_metadata = {}
        if segment_metadata:
            for item in segment_metadata:
                final_segment_metadata.update(item['columns'])
        return final_segment_metadata


    def generate_metrics(self):
        for col in self.columns:
            col.generate_metrics()

    @classmethod
    def sync_to_db_from_config(cls, druid_config, user, cluster):
        """Merges the ds configs from druid_config into one stored in the db."""
        session = get_session()
        datasource = (
            session.query(DruidDatasource)
            .filter_by(
                datasource_name=druid_config['name'])
        ).first()
        # Create a new datasource.
        if not datasource:
            datasource = DruidDatasource(
                datasource_name=druid_config['name'],
                cluster=cluster,
            )
            session.add(datasource)

        dimensions = druid_config['dimensions']
        for dim in dimensions:
            col_obj = (
                session.query(DruidColumn)
                .filter_by(
                    datasource_name=druid_config['name'],
                    column_name=dim)
            ).first()
            if not col_obj:
                col_obj = DruidColumn(
                    datasource_name=druid_config['name'],
                    column_name=dim,
                    groupby=True,
                    filterable=True,
                    # TODO: fetch type from Hive.
                    type="STRING",
                    datasource=datasource
                )
                session.add(col_obj)
        # Import Druid metrics
        for metric_spec in druid_config["metrics_spec"]:
            metric_name = metric_spec["name"]
            metric_type = metric_spec["type"]
            metric_json = json.dumps(metric_spec)

            if metric_type == "count":
                metric_type = "longSum"
                metric_json = json.dumps({
                    "type": "longSum",
                    "name": metric_name,
                    "fieldName": metric_name,
                })

            metric_obj = (
                session.query(DruidMetric)
                .filter_by(
                    datasource_name=druid_config['name'],
                    metric_name=metric_name)
            ).first()
            if not metric_obj:
                metric_obj = DruidMetric(
                    metric_name=metric_name,
                    metric_type=metric_type,
                    verbose_name="%s(%s)" % (metric_type, metric_name),
                    datasource=datasource,
                    json=metric_json,
                    description=(
                        "Imported from the airolap configs dir for %s" %
                        druid_config['name']),
                )
                session.add(metric_obj)
        session.commit()

    @classmethod
    def sync_to_db(cls, name, cluster):
        """Fetches metadata for that datasource and merges the db"""
        logging.info("Syncing Druid datasource [{}]".format(name))
        session = get_session()
        datasource = session.query(cls).filter_by(datasource_name=name).first()
        # print(datasource)
        if not datasource:
            datasource = cls(datasource_name=name)
            session.add(datasource)
        session.commit()
        datasource.cluster = cluster
        session.commit()
        from app.models.druid_column import DruidColumn
        cols = datasource.latest_metadata()
        if not cols:
            logging.error("Failed at fetching the latest segment")
            return
        for col in cols:
            col_obj = (
                session
                .query(DruidColumn)
                .filter_by(datasource_name=name, column_name=col)
                .first()
            )
            datatype = cols[col]['type']
            if not col_obj:
                col_obj = DruidColumn(datasource_name=name, column_name=col)
                session.add(col_obj)
            if datatype == "STRING":
                col_obj.groupby = True
                col_obj.filterable = True
            if datatype == "hyperUnique" or datatype == "thetaSketch":
                col_obj.count_distinct = True
            if col_obj:
                col_obj.type = cols[col]['type']
            session.commit()
            col_obj.datasource = datasource
            col_obj.generate_metrics()
            session.commit()

    @staticmethod
    def time_offset(granularity):
        if granularity == 'week_ending_saturday':
            return 6 * 24 * 3600 * 1000  # 6 days
        return 0

    # uses https://en.wikipedia.org/wiki/ISO_8601
    # http://druid.io/docs/0.8.0/querying/granularities.html
    # TODO: pass origin from the UI
    @staticmethod
    def granularity(period_name, timezone=None, origin=None):
        if not period_name or period_name == 'all':
            return 'all'
        iso_8601_dict = {
            '5 seconds': 'PT5S',
            '30 seconds': 'PT30S',
            '1 minute': 'PT1M',
            '5 minutes': 'PT5M',
            '1 hour': 'PT1H',
            '6 hour': 'PT6H',
            'one day': 'P1D',
            '1 day': 'P1D',
            '7 days': 'P7D',
            'week': 'P1W',
            'week_starting_sunday': 'P1W',
            'week_ending_saturday': 'P1W',
            'month': 'P1M',
        }

        granularity = {'type': 'period'}
        if timezone:
            granularity['timezone'] = timezone

        if origin:
            dttm = utils.parse_human_datetime(origin)
            granularity['origin'] = dttm.isoformat()

        if period_name in iso_8601_dict:
            granularity['period'] = iso_8601_dict[period_name]
            if period_name in ('week_ending_saturday', 'week_starting_sunday'):
                # use Sunday as start of the week
                granularity['origin'] = '2016-01-03T00:00:00'
        elif not isinstance(period_name, string_types):
            granularity['type'] = 'duration'
            granularity['duration'] = period_name
        elif period_name.startswith('P'):
            # identify if the string is the iso_8601 period
            granularity['period'] = period_name
        else:
            granularity['type'] = 'duration'
            granularity['duration'] = utils.parse_human_timedelta(
                period_name).total_seconds() * 1000
        return granularity

    def query(  # druid
            self, groupby, metrics,
            granularity,
            from_dttm, to_dttm,
            filter=None,  # noqa
            is_timeseries=True,
            timeseries_limit=None,
            timeseries_limit_metric=None,
            row_limit=None,
            inner_from_dttm=None, inner_to_dttm=None,
            orderby=None,
            extras=None,  # noqa
            select=None,  # noqa
            columns=None, ):
        """Runs a query against Druid and returns a dataframe.

        This query interface is common to SqlAlchemy and Druid
        """
        # TODO refactor into using a TBD Query object
        qry_start_dttm = datetime.now()
        if not is_timeseries:
            granularity = 'all'
        inner_from_dttm = inner_from_dttm or from_dttm
        inner_to_dttm = inner_to_dttm or to_dttm
        from app import app
        # add tzinfo to native datetime with configs

        from_dttm = utils.parse_human_datetime(from_dttm).replace(tzinfo=app.config.get('DRUID_TZ'))
        to_dttm = utils.parse_human_datetime(to_dttm).replace(tzinfo=app.config.get('DRUID_TZ'))
        timezone = from_dttm.tzname()

        query_str = ""
        metrics_dict = {m.metric_name: m for m in self.metrics}
        all_metrics = []
        post_aggs = {}
        columns_dict = {c.column_name: c for c in self.columns}

        def recursive_get_fields(_conf):
            _fields = _conf.get('fields', [])
            field_names = []
            for _f in _fields:
                _type = _f.get('type')
                if _type in ['fieldAccess', 'hyperUniqueCardinality']:
                    field_names.append(_f.get('fieldName'))
                elif _type == 'arithmetic':
                    field_names += recursive_get_fields(_f)
            return list(set(field_names))

        for metric_name in metrics:
            metric = metrics_dict[metric_name]
            if metric.metric_type != 'postagg':
                all_metrics.append(metric_name)
            else:
                conf = metric.json_obj
                all_metrics += recursive_get_fields(conf)
                all_metrics += conf.get('fieldNames', [])
                if conf.get('type') == 'javascript':
                    post_aggs[metric_name] = JavascriptPostAggregator(
                        name=conf.get('name'),
                        field_names=conf.get('fieldNames'),
                        function=conf.get('function'))
                else:
                    post_aggs[metric_name] = Postaggregator(
                        conf.get('fn', "/"),
                        conf.get('fields', []),
                        conf.get('name', ''))

        # print("columns")
        aggregations = OrderedDict()
        for m in self.metrics:
            if m.metric_name in all_metrics:
                aggregations[m.metric_name] = m.json_obj


        # the dimensions list with dimensionSpecs expanded
        dimensions = []
        groupby = [gb for gb in groupby if gb in columns_dict]
        for column_name in groupby:
            col = columns_dict.get(column_name)
            dim_spec = col.dimension_spec
            if dim_spec:
                dimensions.append(dim_spec)
            else:
                dimensions.append(column_name)
        qry = dict(
            datasource=self.datasource_name,
            dimensions=dimensions,
            aggregations=aggregations,
            granularity=granularity,
            post_aggregations=post_aggs,
            intervals=from_dttm.isoformat() + '/' + to_dttm.isoformat(),
        )
        # """qry = dict(
        #    datasource=self.datasource_name,
        #    dimensions=dimensions,
        #    aggregations=aggregations,
        #    granularity=DruidDatasource.granularity(
        #        granularity,
        #        timezone=timezone,
        #        origin=extras.get('druid_time_origin'),
        #    ),
        #    post_aggregations=post_aggs,
        #    intervals=from_dttm.isoformat() + '/' + to_dttm.isoformat(),
        #)"""
        filterarg_parsed = None
        if filter:
            filterarg_parsed = [tuple(x.split(',')) for x in filter]
        filters = self.get_filters(filterarg_parsed)
        # print("filters")
        having_filters = None
        if filters:
            qry['filter'] = filters
        if extras is None:
            pass
        else:
            having_filters = self.get_having_filters(extras.get('having_druid'))
        if having_filters:
            qry['having'] = having_filters

        client = self.cluster.get_pydruid_client()
        orig_filters = filters
        if len(groupby) == 0:
            del qry['dimensions']
            client.timeseries(**qry)
        if len(groupby) == 1:
            qry['threshold'] = timeseries_limit or 1000
            if row_limit:
                qry['threshold'] = row_limit
            qry['dimension'] = list(qry.get('dimensions'))[0]
            del qry['dimensions']
            qry['metric'] = list(qry['aggregations'].keys())[0]
            client.topn(**qry)
        elif len(groupby) > 1 or having_filters:
            # If grouping on multiple fields or using a having filter
            # we have to force a groupby query
            if timeseries_limit and is_timeseries:
                order_by = metrics[0] if metrics else self.metrics[0]
                if timeseries_limit_metric:
                    order_by = timeseries_limit_metric
                # Limit on the number of timeseries, doing a two-phases query
                pre_qry = deepcopy(qry)
                pre_qry['granularity'] = "all"
                pre_qry['limit_spec'] = {
                    "type": "default",
                    "limit": timeseries_limit,
                    'intervals': (
                        inner_from_dttm.isoformat() + '/' +
                        inner_to_dttm.isoformat()),
                    "columns": [{
                        "dimension": order_by,
                        "direction": "descending",
                    }],
                }
                client.groupby(**pre_qry)
                query_str += "// Two phase query\n// Phase 1\n"
                query_str += json.dumps(
                    client.query_builder.last_query.query_dict, indent=2)
                query_str += "\n"
                query_str += (
                    "//\nPhase 2 (built based on phase one's results)\n")
                df = client.export_pandas()
                if df is not None and not df.empty:
                    dims = qry['dimensions']
                    filters = []
                    for unused, row in df.iterrows():
                        fields = []
                        for dim in dims:
                            f = Dimension(dim) == row[dim]
                            fields.append(f)
                        if len(fields) > 1:
                            filt = Filter(type="and", fields=fields)
                            filters.append(filt)
                        elif fields:
                            filters.append(fields[0])

                    if filters:
                        ff = Filter(type="or", fields=filters)
                        if not orig_filters:
                            qry['filter'] = ff
                        else:
                            qry['filter'] = Filter(type="and", fields=[
                                ff,
                                orig_filters])
                    qry['limit_spec'] = None
            if row_limit:
                qry['limit_spec'] = {
                    "type": "default",
                    "limit": row_limit,
                    "columns": [{
                        "dimension": (
                            metrics[0] if metrics else self.metrics[0]),
                        "direction": "descending",
                    }],
                }
            client.groupby(**qry)
        query_str += json.dumps(
            client.query_builder.last_query.query_dict, indent=2)
        df = client.export_pandas()
        if df is None or df.size == 0:
            raise Exception("No data was returned.")
        df.columns = [
            DTTM_ALIAS if c == 'timestamp' else c for c in df.columns]

        if (
                not is_timeseries and
                granularity == "all" and
                DTTM_ALIAS in df.columns):
            del df[DTTM_ALIAS]

        # Reordering columns
        cols = []
        if DTTM_ALIAS in df.columns:
            cols += [DTTM_ALIAS]
        cols += [col for col in groupby if col in df.columns]
        cols += [col for col in metrics if col in df.columns]
        df = df[cols]

        time_offset = DruidDatasource.time_offset(granularity)

        def increment_timestamp(ts):
            dt = utils.parse_human_datetime(ts).replace(
                tzinfo=app.config.get("DRUID_TZ"))
            return dt + timedelta(milliseconds=time_offset)
        if DTTM_ALIAS in df.columns and time_offset:
            df[DTTM_ALIAS] = df[DTTM_ALIAS].apply(increment_timestamp)
        return QueryResult(
            df=df,
            query=query_str,
            duration=datetime.now() - qry_start_dttm)

    @staticmethod
    def get_filters(raw_filters):
        # print(raw_filters)
        filters = None
        if raw_filters is None:
            filters = None
        else:
            for col, op, eq in raw_filters:
                cond = None
                if op == '==':
                    cond = Dimension(col) == eq
                elif op == '!=':
                    cond = ~(Dimension(col) == eq)
                elif op in ('in', 'not in'):
                    fields = []
                    # Distinguish quoted values with regular value types
                    values = eq.split('|')
                    if len(values) > 1:
                        for s in values:
                            s = s.strip()
                            fields.append(Dimension(col) == s)
                        cond = Filter(type="or", fields=fields)
                    else:
                        cond = Dimension(col) == eq
                    if op == 'not in':
                        cond = ~cond
                elif op == 'regex':
                    cond = Filter(type="regex", pattern=eq, dimension=col)
                if filters:
                    filters = Filter(type="and", fields=[
                        cond,
                        filters
                    ])
                else:
                    filters = cond
        return filters

    def _get_having_obj(self, col, op, eq):
        cond = None
        if op == '==':
            if col in self.column_names:
                cond = DimSelector(dimension=col, value=eq)
            else:
                cond = Aggregation(col) == eq
        elif op == '>':
            cond = Aggregation(col) > eq
        elif op == '<':
            cond = Aggregation(col) < eq

        return cond

    def get_having_filters(self, raw_filters):
        filters = None
        reversed_op_map = {
            '!=': '==',
            '>=': '<',
            '<=': '>'
        }

        for col, op, eq in raw_filters:
            cond = None
            if op in ['==', '>', '<']:
                cond = self._get_having_obj(col, op, eq)
            elif op in reversed_op_map:
                cond = ~self._get_having_obj(col, reversed_op_map[op], eq)

            if filters:
                filters = filters & cond
            else:
                filters = cond
        return filters
