import json
from sqlalchemy import Boolean
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy import Text
from sqlalchemy.orm import relationship, backref

from app.models.basemodel import BaseModel, db
from app.models.druid_cluster import DruidCluster


class DruidMetric(BaseModel):

    """ORM object referencing Druid metrics for a datasource"""

    __tablename__ = 'metrics'
    metric_name = Column(String(512))
    verbose_name = Column(String(1024))
    metric_type = Column(String(32))
    datasource_name = Column(String(255),ForeignKey('druid_datasources.datasource_name'))
    json = Column(Text)
    description = Column(Text)
    is_restricted = Column(Boolean, default=False, nullable=True)
    d3format = Column(String(128))

    @property
    def json_obj(self):
        try:
            obj = json.loads(self.json)
        except Exception:
            obj = {}
        return obj

    @property
    def perm(self):
        return (
            "{parent_name}.[{obj.metric_name}](id:{obj.id})"
        ).format(obj=self,
                 parent_name=self.datasource.full_name
                 ) if self.datasource else None


class DruidColumn(BaseModel):

    """ORM model for storing Druid datasource column metadata"""

    __tablename__ = 'druid_columns'
    datasource_name = Column(String(255),ForeignKey('druid_datasources.datasource_name'))    # Setting enable_typechecks=False disables polymorphic inheritance.
    column_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    type = Column(String(32))
    groupby = Column(Boolean, default=False)
    count_distinct = Column(Boolean, default=False)
    sum = Column(Boolean, default=False)
    avg = Column(Boolean, default=False)
    max = Column(Boolean, default=False)
    min = Column(Boolean, default=False)
    filterable = Column(Boolean, default=False)
    description = Column(Text)
    dimension_spec_json = Column(Text)

    def __repr__(self):
        return self.column_name

    @property
    def isnum(self):
        return self.type in ('LONG', 'DOUBLE', 'FLOAT', 'INT')

    @property
    def dimension_spec(self):
        if self.dimension_spec_json:
            return json.loads(self.dimension_spec_json)

    def generate_metrics(self):
        """Generate metrics based on the column metadata"""
        M = DruidMetric  # noqa
        metrics = []
        metrics.append(DruidMetric(
            metric_name='count',
            verbose_name='COUNT(*)',
            metric_type='count',
            json=json.dumps({'type': 'count', 'name': 'count'})
        ))
        # Somehow we need to reassign this for UDAFs
        if self.type in ('DOUBLE', 'FLOAT'):
            corrected_type = 'DOUBLE'
        else:
            corrected_type = self.type

        if self.sum and self.isnum:
            mt = corrected_type.lower() + 'Sum'
            name = 'sum__' + self.column_name
            metrics.append(DruidMetric(
                metric_name=name,
                metric_type='sum',
                verbose_name='SUM({})'.format(self.column_name),
                json=json.dumps({
                    'type': mt, 'name': name, 'fieldName': self.column_name})
            ))

        if self.avg and self.isnum:
            mt = corrected_type.lower() + 'Avg'
            name = 'avg__' + self.column_name
            metrics.append(DruidMetric(
                metric_name=name,
                metric_type='avg',
                verbose_name='AVG({})'.format(self.column_name),
                json=json.dumps({
                    'type': mt, 'name': name, 'fieldName': self.column_name})
            ))

        if self.min and self.isnum:
            mt = corrected_type.lower() + 'Min'
            name = 'min__' + self.column_name
            metrics.append(DruidMetric(
                metric_name=name,
                metric_type='min',
                verbose_name='MIN({})'.format(self.column_name),
                json=json.dumps({
                    'type': mt, 'name': name, 'fieldName': self.column_name})
            ))
        if self.max and self.isnum:
            mt = corrected_type.lower() + 'Max'
            name = 'max__' + self.column_name
            metrics.append(DruidMetric(
                metric_name=name,
                metric_type='max',
                verbose_name='MAX({})'.format(self.column_name),
                json=json.dumps({
                    'type': mt, 'name': name, 'fieldName': self.column_name})
            ))
        if self.count_distinct:
            name = 'count_distinct__' + self.column_name
            if self.type == 'hyperUnique' or self.type == 'thetaSketch':
                metrics.append(DruidMetric(
                    metric_name=name,
                    verbose_name='COUNT(DISTINCT {})'.format(self.column_name),
                    metric_type=self.type,
                    json=json.dumps({
                        'type': self.type,
                        'name': name,
                        'fieldName': self.column_name
                    })
                ))
            else:
                mt = 'count_distinct'
                metrics.append(DruidMetric(
                    metric_name=name,
                    verbose_name='COUNT(DISTINCT {})'.format(self.column_name),
                    metric_type='count_distinct',
                    json=json.dumps({
                        'type': 'cardinality',
                        'name': name,
                        'fieldNames': [self.column_name]})
                ))
        session = db.session()
        new_metrics = []
        for metric in metrics:
            m = (
                session.query(M)
                .filter(M.metric_name == metric.metric_name)
                .filter(M.datasource_name == self.datasource_name)
                .filter(DruidCluster.cluster_name == self.datasource.cluster_name)
                .first()
            )
            metric.datasource_name = self.datasource_name
            if not m:
                new_metrics.append(metric)
                session.add(metric)
                session.flush()
