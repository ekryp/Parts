import json
import os
from datetime import datetime
from app.auth.authorization import requires_auth
import pandas as pd
from app import Configuration
from app import app
from app import csvs, excel, mytext
from app.tasks import celery, add_prospect, update_prospect_step
from app.utils.utils import get_df_from_sql_query
from flask import jsonify
from flask import request
from flask_restful import Resource
from flask_restful import reqparse
from sqlalchemy import create_engine
from app.tasks import derive_table_creation


class GetSparePartAnalysis(Resource):

    @requires_auth
    def get(self):
        engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args)
        query = "SELECT distinct(end_cust_name) FROM end_customer"
        end_customer_name_df = pd.read_sql(query, engine)
        customer_names = end_customer_name_df['end_cust_name'].tolist()
        query = "SELECT distinct(analysis_type_name)  FROM analysis_type"
        analysis_names_df = pd.read_sql(query, engine)
        analysis_names = analysis_names_df['analysis_type_name'].tolist()
        query = "SELECT distinct(replenish_time_name) FROM replenish_table"
        replenish_times_df = pd.read_sql(query, engine)
        replenish_times = replenish_times_df['replenish_time_name'].tolist()
        response = {
            "customer_names": customer_names,
            "analysis_names": analysis_names,
            "replenish_times": replenish_times
        }
        return response


class GetstepsAllUsers(Resource):

    @requires_auth
    def get(self):
        query = "SELECT  *  FROM prospect_details as a " \
                "right join prospect_status as b " \
                "on a.prospects_id = b.prospects_id " \
                "right join prospect_steps as c " \
                "on c.step_id = b.prospects_step " \
                "right join analysis_request as d on " \
                "d.analysis_request_time = b.analysis_request_time " \
                "where prospects_email is NOT NULL order by prospects_email"


        result = get_df_from_sql_query(
            query=query,
            db_connection_string=Configuration.INFINERA_DB_URL)

        result = result.loc[:, ~result.columns.duplicated()]
        #Removes duplicate column names not column values
        response = json.loads(result.to_json(orient="records", date_format='iso'))
        return response


class GetstepsforSpecificRequest(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('request_id', type=int, required=True, help='id', location='args')
        super(GetstepsforSpecificRequest, self).__init__()

    @requires_auth
    def get(self):
        args = self.reqparse.parse_args()
        request_id = args['request_id']
        query = "SELECT  *  FROM prospect_details as a " \
                "right join prospect_status as b " \
                "on a.prospects_id = b.prospects_id " \
                "right join prospect_steps as c " \
                "on c.step_id = b.prospects_step " \
                "right join analysis_request as d on " \
                "d.analysis_request_time = b.analysis_request_time " \
                "where prospects_email is NOT NULL and analysis_request_id = {0} " \
                "order by prospects_email".format(request_id)


        result = get_df_from_sql_query(
            query=query,
            db_connection_string=Configuration.INFINERA_DB_URL)

        result = result.loc[:, ~result.columns.duplicated()]
        #Removes duplicate column names not column values
        response = json.loads(result.to_json(orient="records", date_format='iso'))
        return response


class GetSummaryforSpecificRequest(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('request_id', type=int, required=True, help='id', location='args')
        self.reqparse.add_argument('toggle', type=str, required=True, location='args')
        super(GetSummaryforSpecificRequest, self).__init__()

    @requires_auth
    def get(self):
        args = self.reqparse.parse_args()
        request_id = args['request_id']
        toggle = args['toggle']
        # toggle is True by default meaning by default reorder
        # False means total_stock
        if toggle == 'reorder':
            # Find Current Gross
            gross_query = 'SELECT part_name,depot_name,pon_quantity as gross_qty,request_id FROM mtbf_bom_calculated ' \
                    'where pon_quantity > 0 and request_id={0} order by gross_qty desc'.format(request_id)

            gross_df = get_df_from_sql_query(
                query=gross_query,
                db_connection_string=Configuration.INFINERA_DB_URL)

            # Find Current Inventory reorder

            current_inv_query = 'select part_name,depot_name,sum(reorder_point) as qty, ' \
                                'sum(used_spare_count_reorder) as spare_count, ' \
                                'High_spare_reoderpoint_cost as ext_spare_cost from summary as a ' \
                    'right join analysis_request as b on a.request_id = b.analysis_request_id ' \
                    'where b.requestStatus="Completed" and reorder_point!=0 and a.request_id = {0} ' \
                    'group by part_name,depot_name,reorder_point;'.format(request_id)

            current_inv = get_df_from_sql_query(
                query=current_inv_query,
                db_connection_string=Configuration.INFINERA_DB_URL)

            net_df = pd.merge(gross_df, current_inv, on=['part_name', 'depot_name'], how='left')

            net_df['qty'].fillna(0, inplace=True)

            # Net = Current - Gross
            net_df['net_qty'] = net_df['qty'] - net_df['gross_qty']

            # Take Only shortage,ignore surplus
            # net_df = net_df[net_df['net_qty'] < 0]

            # Make surplus as zero quantity
            net_df.loc[net_df['net_qty'] > 0, 'net_qty'] = 0

            net_df['net_qty'] = net_df['net_qty'].abs()

            summary_df_query = 'select part_name, depot_name, material_number,high_spare, customer_name, ' \
                         'standard_cost from summary where request_id={0}'.format(request_id)

            summary_df = get_df_from_sql_query(
                query=summary_df_query,
                db_connection_string=Configuration.INFINERA_DB_URL)

            summary_df = pd.merge(net_df, summary_df, on=['part_name', 'depot_name'], how='left')
            summary_df['spare_count'].fillna(0, inplace=True)
            summary_df['ext_spare_cost'].fillna(0, inplace=True)
            summary_df['net_std_cost'] = summary_df['net_qty'] * summary_df['standard_cost']

            # get IB quantities & std_gross_cost in summary_df
            ib_query = 'SELECT product_ordering_name, node_depot_belongs, pon_quanity as ib_quantity' \
                    ' FROM current_ib where pon_quanity>0 and request_id = {0}'.format(request_id)

            ib_df = get_df_from_sql_query(
                query=ib_query,
                db_connection_string=Configuration.INFINERA_DB_URL)

            summary_df = pd.merge(summary_df, ib_df, left_on=['part_name', 'depot_name'],
                                  right_on=['product_ordering_name', 'node_depot_belongs'], how='left')

            summary_df.loc[summary_df['ib_quantity'].isna(), 'ib_quantity'] = 0
            summary_df = summary_df.drop(['request_id', 'product_ordering_name', 'node_depot_belongs'], 1)

            summary_df['std_gross_cost'] = summary_df['standard_cost'] * summary_df['gross_qty']
            #summary_df['ext_spare_cost'] = summary_df['standard_cost'] * summary_df['spare_count']
            summary_df.sort_values(by=['net_qty'], ascending=False, inplace=True)
            response = json.loads(summary_df.to_json(orient="records", date_format='iso'))
            return response

        else:
            # Find Current Gross
            gross_query = 'SELECT part_name,depot_name,pon_quantity as gross_qty, request_id FROM mtbf_bom_calculated ' \
                          'where pon_quantity > 0 and request_id={0} order by gross_qty desc'.format(request_id)

            gross_df = get_df_from_sql_query(
                query=gross_query,
                db_connection_string=Configuration.INFINERA_DB_URL)

            current_inv_query = 'select part_name,depot_name,sum(total_stock) as qty,' \
                                ' sum(used_spare_count_total_stock) as spare_count,' \
                                'High_spare_totalstock_cost as ext_spare_cost from summary as a ' \
                    'right join analysis_request as b on a.request_id = b.analysis_request_id ' \
                    'where b.requestStatus="Completed" and total_stock!=0 and a.request_id = {0} ' \
                    'group by part_name,depot_name,total_stock;'.format(request_id)

            current_inv = get_df_from_sql_query(
                query=current_inv_query,
                db_connection_string=Configuration.INFINERA_DB_URL)

            net_df = pd.merge(gross_df, current_inv, on=['part_name', 'depot_name'], how='left')

            net_df['qty'].fillna(0, inplace=True)

            # Net = Current - Gross
            net_df['net_qty'] = net_df['qty'] - net_df['gross_qty']

            # Take Only shortage,ignore surplus
            # net_df = net_df[net_df['net_qty'] < 0]

            # Make surplus as zero quantity
            net_df.loc[net_df['net_qty'] > 0, 'net_qty'] = 0

            net_df['net_qty'] = net_df['net_qty'].abs()

            summary_df_query = 'select part_name, depot_name, material_number,high_spare, customer_name, ' \
                         'standard_cost from summary where request_id={0}'.format(request_id)

            summary_df = get_df_from_sql_query(
                query=summary_df_query,
                db_connection_string=Configuration.INFINERA_DB_URL)

            summary_df = pd.merge(net_df, summary_df, on=['part_name', 'depot_name'], how='left')
            summary_df['spare_count'].fillna(0, inplace=True)
            summary_df['ext_spare_cost'].fillna(0, inplace=True)
            summary_df['net_std_cost'] = summary_df['net_qty'] * summary_df['standard_cost']

            # get IB quantities & std_gross_cost in summary_df
            ib_query = 'SELECT product_ordering_name, node_depot_belongs, pon_quanity as ib_quantity' \
                       ' FROM current_ib where pon_quanity>0 and request_id = {0}'.format(request_id)

            ib_df = get_df_from_sql_query(
                query=ib_query,
                db_connection_string=Configuration.INFINERA_DB_URL)

            summary_df = pd.merge(summary_df, ib_df, left_on=['part_name', 'depot_name'],
                                  right_on=['product_ordering_name', 'node_depot_belongs'], how='left')

            summary_df.loc[summary_df['ib_quantity'].isna(), 'ib_quantity'] = 0
            summary_df = summary_df.drop(['request_id', 'product_ordering_name', 'node_depot_belongs'], 1)

            summary_df['std_gross_cost'] = summary_df['standard_cost'] * summary_df['gross_qty']
            #summary_df['ext_spare_cost'] = summary_df['standard_cost'] * summary_df['spare_count']
            summary_df.sort_values(by=['net_qty'], ascending=False, inplace=True)
            response = json.loads(summary_df.to_json(orient="records", date_format='iso'))
            return response


class GetGrossforSpecificRequest(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('request_id', type=int, required=True, help='id', location='args')
        super(GetGrossforSpecificRequest, self).__init__()

    @requires_auth
    def get(self):

        args = self.reqparse.parse_args()
        request_id = args['request_id']

        query = 'SELECT part_name,depot_name,pon_quantity as gross_qty FROM mtbf_bom_calculated ' \
                'where pon_quantity > 0 and request_id={0} order by gross_qty desc'.format(request_id)

        print(query)

        result = get_df_from_sql_query(
            query=query,
            db_connection_string=Configuration.INFINERA_DB_URL)

        response = json.loads(result.to_json(orient="records", date_format='iso'))
        return response


class GetCurrentIB(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('request_id', type=int, required=True, help='id', location='args')
        super(GetCurrentIB, self).__init__()

    @requires_auth
    def get(self):

        args = self.reqparse.parse_args()
        request_id = args['request_id']

        query = 'SELECT product_ordering_name, node_depot_belongs, pon_quanity' \
                ' FROM current_ib where pon_quanity>0 and request_id = {0}'.format(request_id)

        print(query)

        result = get_df_from_sql_query(
            query=query,
            db_connection_string=Configuration.INFINERA_DB_URL)

        response = json.loads(result.to_json(orient="records", date_format='iso'))
        return response


class GetCurrentInventory(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('request_id', type=int, required=True, help='id', location='args')
        self.reqparse.add_argument('toggle', type=str, required=True, location='args')
        super(GetCurrentInventory, self).__init__()

    @requires_auth
    def get(self):

        args = self.reqparse.parse_args()
        request_id = args['request_id']
        toggle = args['toggle']

        # toggle is True by default meaning by default reorder
        # False means total_stock
        if toggle == 'reorder':
            query = 'select part_name,depot_name,sum(reorder_point) as qty from summary as a ' \
                    'right join analysis_request as b on a.request_id = b.analysis_request_id ' \
                    'where b.requestStatus="Completed" and reorder_point!=0 and a.request_id = {0} ' \
                    'group by part_name,depot_name,reorder_point;'.format(request_id)
        else:
            query = 'select part_name,depot_name,sum(total_stock) as qty from summary as a ' \
                    'right join analysis_request as b on a.request_id = b.analysis_request_id ' \
                    'where b.requestStatus="Completed" and total_stock!=0 and a.request_id = {0} ' \
                    'group by part_name,depot_name,total_stock;'.format(request_id)

        print(query)

        result = get_df_from_sql_query(
            query=query,
            db_connection_string=Configuration.INFINERA_DB_URL)

        response = json.loads(result.to_json(orient="records", date_format='iso'))
        return response


class GetCurrentNet(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('request_id', type=int, required=True, help='id', location='args')
        self.reqparse.add_argument('toggle', type=str, required=True, location='args')
        super(GetCurrentNet, self).__init__()

    @requires_auth
    def get(self):

        args = self.reqparse.parse_args()
        request_id = args['request_id']
        toggle = args['toggle']

        # toggle is True by default meaning by default reorder
        # False means total_stock

        if toggle == 'reorder':
            # Find Current Gross
            gross_query = 'SELECT part_name,depot_name,pon_quantity as gross_qty FROM mtbf_bom_calculated ' \
                    'where pon_quantity > 0 and request_id={0} order by gross_qty desc'.format(request_id)

            gross_df = get_df_from_sql_query(
                query=gross_query,
                db_connection_string=Configuration.INFINERA_DB_URL)

            # Find Current Inventory reorder

            current_inv_query = 'select part_name,depot_name,sum(reorder_point) as qty from summary as a ' \
                    'right join analysis_request as b on a.request_id = b.analysis_request_id ' \
                    'where b.requestStatus="Completed" and reorder_point!=0 and a.request_id = {0} ' \
                    'group by part_name,depot_name,reorder_point;'.format(request_id)

            current_inv = get_df_from_sql_query(
                query=current_inv_query,
                db_connection_string=Configuration.INFINERA_DB_URL)

            net_df = pd.merge(gross_df, current_inv, on=['part_name', 'depot_name'], how='left')

            net_df['qty'].fillna(0, inplace=True)

            # Net = Current - Gross
            net_df['net_qty'] = net_df['qty'] - net_df['gross_qty']

            # Take Only shortage,ignore surplus
            net_df = net_df[net_df['net_qty'] < 0]

            # Keep only required columns
            net_df = net_df[['part_name', 'depot_name', 'net_qty']]

            net_df['net_qty'] = net_df['net_qty'].abs()
            response = json.loads(net_df.to_json(orient="records", date_format='iso'))
            return response


        else:
            # Find Current Gross
            gross_query = 'SELECT part_name,depot_name,pon_quantity as gross_qty FROM mtbf_bom_calculated ' \
                          'where pon_quantity > 0 and request_id={0} order by gross_qty desc'.format(request_id)

            gross_df = get_df_from_sql_query(
                query=gross_query,
                db_connection_string=Configuration.INFINERA_DB_URL)

            current_inv_query = 'select part_name,depot_name,sum(total_stock) as qty from summary as a ' \
                    'right join analysis_request as b on a.request_id = b.analysis_request_id ' \
                    'where b.requestStatus="Completed" and total_stock!=0 and a.request_id = {0} ' \
                    'group by part_name,depot_name,total_stock;'.format(request_id)

            current_inv = get_df_from_sql_query(
                query=current_inv_query,
                db_connection_string=Configuration.INFINERA_DB_URL)

            net_df = pd.merge(gross_df, current_inv, on=['part_name', 'depot_name'], how='left')

            net_df['qty'].fillna(0, inplace=True)

            # Net = Current - Gross
            net_df['net_qty'] = net_df['qty'] - net_df['gross_qty']

            # Take Only shortage,ignore surplus
            net_df = net_df[net_df['net_qty'] < 0]

            # Keep only required columns
            net_df = net_df[['part_name', 'depot_name', 'net_qty']]

            net_df['net_qty'] = net_df['net_qty'].abs()
            response = json.loads(net_df.to_json(orient="records", date_format='iso'))
            return response


class GetDashboardRequestCount(Resource):

    @requires_auth
    def get(self):

        def get_respective_counts():
            engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args)

            total_request_query = "select count(*) from analysis_request"
            total_request = engine.execute(total_request_query).fetchone()[0]

            incomplete_request_query = "select count(*) from analysis_request where requestStatus = 'Processing'"
            incomplete_request = engine.execute(incomplete_request_query).fetchone()[0]

            complete_request_query = "select count(*) from analysis_request where requestStatus = 'Completed'"
            complete_request = engine.execute(complete_request_query).fetchone()[0]

            failed_request_query = "select count(*) from analysis_request where requestStatus = 'Failed'"
            failed_request = engine.execute(failed_request_query).fetchone()[0]

            saved_request = 0
            complete_request_succesfully = complete_request
            return total_request,incomplete_request, complete_request, failed_request, saved_request, complete_request_succesfully

        total_request, incomplete_request, complete_request, failed_request, saved_request, complete_request_succesfully = get_respective_counts()

        response = {
            'total_request': total_request,
            'incomplete_request': incomplete_request,
            'complete_request': complete_request,
            'failed_request': failed_request,
            'saved_request': saved_request,
            'complete_request_succesfully': complete_request_succesfully
        }
        return response


class GetMainDashboardCount(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('toggle', type=str, required=False, location='args', default='reorder')
        super(GetMainDashboardCount, self).__init__()

    @requires_auth
    def get(self):
        args = self.reqparse.parse_args()
        toggle = args['toggle']
        print(toggle)
        # toggle is True by default meaning by default reorder
        # False means total_stock
        if toggle == 'reorder':

            def get_respective_counts():
                engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args)

                total_customer_query = 'SELECT count(distinct(customer_name)) FROM summary where is_latest= "Y";'
                total_customer = engine.execute(total_customer_query).fetchone()[0]

                total_pon_type_query = 'SELECT count(distinct(part_name))  FROM summary where is_latest= "Y";'
                total_pon_type = engine.execute(total_pon_type_query).fetchone()[0]

                total_depot_query = 'select  count(distinct(depot_name))  FROM summary where is_latest= "Y"'
                total_depot = engine.execute(total_depot_query).fetchone()[0]

                critical_pon_query = 'select  count(distinct(part_name))  FROM summary where  ' \
                                     'net_reorder_point >0 and is_latest= "Y"'
                critical_pon = engine.execute(critical_pon_query).fetchone()[0]

                critical_customer_query = 'select  count(distinct(customer_name))  FROM summary where' \
                                          '  net_reorder_point >0 and is_latest= "Y"'
                critical_customer = engine.execute(critical_customer_query).fetchone()[0]

                critical_depot_query = 'select count(distinct(depot_name)) FROM summary ' \
                                       'where  net_reorder_point >0 and is_latest= "Y"'
                critical_depot = engine.execute(critical_depot_query).fetchone()[0]

                return total_customer, critical_pon, critical_customer, critical_depot, total_pon_type, total_depot

            total_customer, critical_pon, critical_customer, critical_depot, total_pon_type, total_depot = get_respective_counts()

            response = {
                'total_customer': total_customer,
                'critical_pon': critical_pon,
                'critical_customer': critical_customer,
                'critical_depot': critical_depot,
                'total_pon_type': total_pon_type,
                'total_depot': total_depot
            }
            return response

        else:
            def get_respective_counts():
                engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args)

                total_customer_query = 'SELECT count(distinct(customer_name)) FROM summary where is_latest= "Y";'
                total_customer = engine.execute(total_customer_query).fetchone()[0]

                total_pon_type_query = 'SELECT count(distinct(part_name))  FROM summary where is_latest= "Y";'
                total_pon_type = engine.execute(total_pon_type_query).fetchone()[0]

                total_depot_query = 'select  count(distinct(depot_name))  FROM summary where is_latest= "Y"'
                total_depot = engine.execute(total_depot_query).fetchone()[0]

                critical_pon_query = 'select  count(distinct(part_name))  FROM summary where  ' \
                                     ' net_total_stock > 0 and is_latest= "Y";'
                critical_pon = engine.execute(critical_pon_query).fetchone()[0]

                critical_customer_query = 'select  count(distinct(customer_name))  FROM summary where' \
                                          '  net_total_stock > 0 and is_latest= "Y";'
                critical_customer = engine.execute(critical_customer_query).fetchone()[0]

                critical_depot_query = 'select count(distinct(depot_name)) FROM summary ' \
                                       'where  net_total_stock > 0 and is_latest= "Y"'
                critical_depot = engine.execute(critical_depot_query).fetchone()[0]

                return total_customer, critical_pon, critical_customer, critical_depot, total_pon_type, total_depot

            total_customer, critical_pon, critical_customer, critical_depot, total_pon_type, total_depot = get_respective_counts()

            response = {
                'total_customer': total_customer,
                'critical_pon': critical_pon,
                'critical_customer': critical_customer,
                'critical_depot': critical_depot,
                'total_pon_type': total_pon_type,
                'total_depot': total_depot
            }
            return response




class GetPieChart(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('toggle', type=str, required=False, location='args', default='reorder')
        super(GetPieChart, self).__init__()

    @requires_auth
    def get(self):
        args = self.reqparse.parse_args()
        toggle = args['toggle']
        print(toggle)
        # toggle is True by default meaning by default reorder
        # False means total_stock
        if toggle == 'reorder':

            def get_respective_counts():
                engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args)

                non_critical_pon_query = 'select  count((part_name))  FROM summary  where  ' \
                                     'net_reorder_point = 0 and is_latest="Y"'
                non_critical_pon = engine.execute(non_critical_pon_query).fetchone()[0]

                critical_pon_query ='select  count((part_name))  FROM summary   where  ' \
                          'net_reorder_point > 0 and is_latest="Y"'
                critical_pon = engine.execute(critical_pon_query).fetchone()[0]

                return non_critical_pon, critical_pon

            non_critical_pon, critical_pon = get_respective_counts()

            response = {
                'non_critical_pon': non_critical_pon,
                'critical_pon': critical_pon,

            }
            return response

        else:

            def get_respective_counts():
                engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args)

                non_critical_pon_query = 'select  count((part_name))  FROM summary  where  ' \
                                     'net_total_stock = 0 and is_latest="Y"'
                non_critical_pon = engine.execute(non_critical_pon_query).fetchone()[0]

                critical_pon_query ='select  count((part_name))  FROM summary   where  ' \
                          ' net_total_stock >0 and is_latest="Y"'

                critical_pon = engine.execute(critical_pon_query).fetchone()[0]

                return non_critical_pon, critical_pon

            non_critical_pon, critical_pon = get_respective_counts()

            response = {
                'non_critical_pon': non_critical_pon,
                'critical_pon': critical_pon,

            }
            return response


class GetTopPons(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('toggle', type=str, required=False, location='args', default='reorder')
        super(GetTopPons, self).__init__()

    @requires_auth
    def get(self):
        args = self.reqparse.parse_args()
        toggle = args['toggle']
        print(toggle)
        # toggle is True by default meaning by default reorder
        # False means total_stock
        if toggle == 'reorder':

            query = 'select part_name,count(*) as critical_pon_count FROM summary   where' \
                '  net_reorder_point >0  and is_latest="Y" group by part_name order by ' \
                    'critical_pon_count desc'

            result = get_df_from_sql_query(
                query=query,
                db_connection_string=Configuration.INFINERA_DB_URL)

            response = json.loads(result.to_json(orient="records", date_format='iso'))
            return response

        else:

            query = 'select part_name,count(*) as critical_pon_count FROM summary   where' \
                '  net_total_stock >0  and is_latest="Y" group by part_name order by ' \
                    'critical_pon_count desc'

            result = get_df_from_sql_query(
                query=query,
                db_connection_string=Configuration.INFINERA_DB_URL)

            response = json.loads(result.to_json(orient="records", date_format='iso'))
            return response


class GetTopDepots(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('toggle', type=str, required=False, location='args', default='reorder')
        super(GetTopDepots, self).__init__()

    @requires_auth
    def get(self):
        args = self.reqparse.parse_args()
        toggle = args['toggle']
        print(toggle)
        # toggle is True by default meaning by default reorder
        # False means total_stock
        if toggle == 'reorder':
            query = 'select depot_name,count(part_name) as critical_pon_count FROM summary   ' \
                    'where (net_reorder_point >0) and is_latest="Y" group by depot_name order by ' \
                    'critical_pon_count desc'

            result = get_df_from_sql_query(
                query=query,
                db_connection_string=Configuration.INFINERA_DB_URL)

            response = json.loads(result.to_json(orient="records", date_format='iso'))
            return response

        else:

            query = 'select depot_name,count(part_name) as critical_pon_count FROM summary   ' \
                    'where (net_total_stock >0) and is_latest="Y" group by depot_name order by ' \
                    'critical_pon_count desc'

            result = get_df_from_sql_query(
                query=query,
                db_connection_string=Configuration.INFINERA_DB_URL)

            response = json.loads(result.to_json(orient="records", date_format='iso'))
            return response


class GetTopCustomer(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('toggle', type=str, required=False, location='args', default='reorder')
        super(GetTopCustomer, self).__init__()

    @requires_auth
    def get(self):

        args = self.reqparse.parse_args()
        toggle = args['toggle']
        print(toggle)
        # toggle is True by default meaning by default reorder
        # False means total_stock
        if toggle == 'reorder':
            query = 'select customer_name,count(part_name) as critical_pon_count FROM summary  ' \
                ' where  net_reorder_point >0 and is_latest="Y" ' \
                'group by customer_name order by critical_pon_count desc'

            result = get_df_from_sql_query(
                query=query,
                db_connection_string=Configuration.INFINERA_DB_URL)

            response = json.loads(result.to_json(orient="records", date_format='iso'))
            return response

        else:
            query = 'select customer_name,count(part_name) as critical_pon_count FROM summary  ' \
                ' where  net_total_stock >0 and is_latest="Y" ' \
                'group by customer_name order by critical_pon_count desc'

            result = get_df_from_sql_query(
                query=query,
                db_connection_string=Configuration.INFINERA_DB_URL)

            response = json.loads(result.to_json(orient="records", date_format='iso'))
            return response


class GetTopExtended(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('toggle', type=str, required=False, location='args', default='reorder')
        super(GetTopExtended, self).__init__()

    @requires_auth
    def get(self):

        args = self.reqparse.parse_args()
        toggle = args['toggle']
        print(toggle)
        # toggle is True by default meaning by default reorder
        # False means total_stock
        if toggle == 'reorder':

            query = 'select part_name,depot_name,customer_name,count(*) as critical_pon_count FROM summary ' \
                    'where  net_reorder_point>0 and is_latest="Y" group by part_name,depot_name,' \
                    'customer_name ' \
                    'order by critical_pon_count desc'

            result = get_df_from_sql_query(
                query=query,
                db_connection_string=Configuration.INFINERA_DB_URL)

            response = json.loads(result.to_json(orient="records", date_format='iso'))
            return response

        else:

            query = 'select part_name,depot_name,customer_name,count(*) as critical_pon_count FROM summary ' \
                    'where  net_total_stock>0 and is_latest="Y" group by part_name,depot_name,' \
                    'customer_name ' \
                    'order by critical_pon_count desc'

            result = get_df_from_sql_query(
                query=query,
                db_connection_string=Configuration.INFINERA_DB_URL)

            response = json.loads(result.to_json(orient="records", date_format='iso'))
            return response


class GetLatLon(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('toggle', type=str, required=False, location='args', default='reorder')
        super(GetLatLon, self).__init__()

    @requires_auth
    def get(self):

        args = self.reqparse.parse_args()
        toggle = args['toggle']
        print(toggle)
        # toggle is True by default meaning by default reorder
        # False means total_stock
        if toggle == 'reorder':

            query = 'SELECT a.depot_name,b.lat,b.long,count(part_name) as critical_pon_count  FROM summary as a' \
                    ' right join depot as b on a.depot_name= b.depot_name where a.depot_name is not null and ' \
                    'b.lat is not null and b.long is not null and net_reorder_point >0 and is_latest="Y" ' \
                    'group by depot_name order by critical_pon_count desc'

            result = get_df_from_sql_query(
                query=query,
                db_connection_string=Configuration.INFINERA_DB_URL)

            response = json.loads(result.to_json(orient="records", date_format='iso'))
            return response

        else:
            query = 'SELECT a.depot_name,b.lat,b.long,count(part_name) as critical_pon_count  FROM summary as a' \
                    ' right join depot as b on a.depot_name= b.depot_name where a.depot_name is not null and ' \
                    'b.lat is not null and b.long is not null and net_total_stock >0 and is_latest="Y" ' \
                    'group by depot_name order by critical_pon_count desc'

            result = get_df_from_sql_query(
                query=query,
                db_connection_string=Configuration.INFINERA_DB_URL)

            response = json.loads(result.to_json(orient="records", date_format='iso'))
            return response


class GetAnalysisName(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('request_id', type=int, required=True, help='id', location='args')
        super(GetAnalysisName, self).__init__()

    @requires_auth
    def get(self):
        args = self.reqparse.parse_args()
        request_id = args['request_id']

        query = 'SELECT analysis_name FROM analysis_request where analysis_request_id={0}'.format(request_id)

        result = get_df_from_sql_query(
            query=query,
            db_connection_string=Configuration.INFINERA_DB_URL)

        response = json.loads(result.to_json(orient="records", date_format='iso'))
        return response


class GetErrorRecords(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('request_id', type=int, required=True, help='id', location='args')
        super(GetErrorRecords, self).__init__()

    @requires_auth
    def get(self):
        args = self.reqparse.parse_args()
        request_id = args['request_id']

        query = 'SELECT  error_reason,type,PON,node_name  FROM error_records where request_id={0}'.format(request_id)

        result = get_df_from_sql_query(
            query=query,
            db_connection_string=Configuration.INFINERA_DB_URL)

        response = json.loads(result.to_json(orient="records", date_format='iso'))
        return response


class FileFormatIssue(Exception):
    def __init__(self, filename, msg):
        self.filename = filename
        self.msg = msg


class PostSparePartAnalysis(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('analysis_name', required=True, location='form')
        self.reqparse.add_argument('analysis_type', required=True, location='form')
        self.reqparse.add_argument('replenish_time', required=True, location='form')
        self.reqparse.add_argument('customer_name', required=True, location='form')
        self.reqparse.add_argument('user_email_id', required=True, location='form')
        self.reqparse.add_argument('replenish_time', required=True, location='form')
        super(PostSparePartAnalysis, self).__init__()

    @requires_auth
    def post(self):

        args = self.reqparse.parse_args()
        dest_folder = request.form.get('user_email_id')
        analysis_date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        customer_dna_file = ''
        sap_export_file = ''
        customer_name = args['customer_name'].replace(",", "|")
        replenish_time = args['replenish_time'].replace(",", "|")

        def save_analysis_record_db():

            engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args)
            query = "INSERT INTO analysis_request (cust_id, analysis_name, analysis_type, " \
                    "replenish_time, user_email_id, analysis_request_time, dna_file_name, " \
                    "current_inventory_file_name, customer_name) values ({0},'{1}','{2}','{3}','{4}','{5}'," \
                    "'{6}','{7}','{8}')".format(7, args['analysis_name'], args['analysis_type'],
                                                replenish_time,
                                                args['user_email_id'], analysis_date,
                                                customer_dna_file, sap_export_file,
                                                customer_name)
            engine.execute(query)

        def get_analysis_id():
            engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args)
            query = 'SELECT max(analysis_request_id) FROM analysis_request;'
            result = engine.execute(query).fetchone()
            return result[0]

        def check_header_sap_file(sap_file, filename, file_location):

            try:
                sap_inventory_data = pd.read_excel(sap_file, sheet_name='Sheet1')
            except Exception as e:
                raise FileFormatIssue(filename, "Current Inventory File Corrupt or Sheet1 is not present,BAD Current Inventory File")

            rows, columns = sap_inventory_data.shape
            if rows < 1:
                raise FileFormatIssue(filename, "No Records to process,BAD Current Inventory File")
            
            if len(sap_inventory_data.columns) < 10:
                    raise FileFormatIssue(filename, "Number of columns is less than minimum columns 10, BAD Current Inventory File")
            '''
            our_columns = ['Plant', 'Storage Location = Depot Name', 'Material Number', 'Material Description = Part Name',
                       'Total Stock', 'Reorder Point', 'Standard Cost', 'Total Standard Cost', 'STO - Qty To be Dlv.',
                       'Delivery - Qty To be Dlv.']

            infinera_columns = ['Material Number', 'Material Description', 'Plant', 'Storage Location',
                                'Reorder Point', 'Total Stock', 'Standard Cost', 'Total Standard Cost',
                                'STO - Qty To be Dlv.', 'Delivery - Qty To be Dlv.']
            sap_inventory_data.rename(columns={
                    'Material Description': 'Material Description = Part Name',
                    'Storage Location': 'Storage Location = Depot Name',
                                    }, inplace=True
                                    )

            sap_inventory_data.to_excel(os.path.join(file_location, filename), index=False)
            '''

        def check_dna_file(dna_file, extension):
            if extension.lower() == '.csv':
                dna_df = pd.read_csv(dna_file, nrows=200)

            elif extension.lower() == '.txt':
                dna_df = pd.read_csv(dna_file, sep='\t', nrows=200)

            elif extension.lower() == '.xls' or extension.lower() == '.xlsx':
                dna_df = pd.read_excel(dna_file)

            dna_row, dna_cols = dna_df.shape
            if dna_row < 1:
                raise FileFormatIssue(dna_file, "No Records to process,BAD DNA File")



        try:

            for file in request.files.getlist('customer_dna_file'):

                name, extension = os.path.splitext(file.filename)

                if extension.lower() == '.csv':
                    dir_path = os.path.join(app.config.get("UPLOADED_CSV_DEST"), dest_folder)
                    full_path = os.path.abspath(dir_path)
                    file.filename = "customer_dna_file_{0}{1}".format(analysis_date, extension.lower())
                    customer_dna_file = file.filename
                    csvs.save(file, folder=dest_folder)

                elif extension.lower() == '.xls' or extension.lower() == '.xlsx':
                    dir_path = os.path.join(app.config.get("UPLOADED_EXCEL_DEST"), dest_folder)
                    full_path = os.path.abspath(dir_path)
                    file.filename = "customer_dna_file_{0}{1}".format(analysis_date, extension.lower())
                    customer_dna_file = file.filename
                    excel.save(file, folder=dest_folder)

                elif extension.lower() == '.txt':
                    dir_path = os.path.join(app.config.get("UPLOADED_TEXT_DEST"), dest_folder)
                    full_path = os.path.abspath(dir_path)
                    file.filename = "customer_dna_file_{0}{1}".format(analysis_date, extension.lower())
                    customer_dna_file = file.filename
                    mytext.save(file, folder=dest_folder)

                dna_file = os.path.join(full_path, customer_dna_file)
                check_dna_file(dna_file, extension)

            for file in request.files.getlist('sap_export_file'):

                name, extension = os.path.splitext(file.filename)

                if extension.lower() == '.csv':

                    raise FileFormatIssue('SAP_FILE', "Please upload Excel file, BAD Current Inventory File")
                    dir_path = os.path.join(app.config.get("UPLOADED_CSV_DEST"), dest_folder)
                    full_path = os.path.abspath(dir_path)
                    file.filename = "sap_export_file{0}{1}".format(analysis_date, extension.lower())
                    sap_export_file = file.filename
                    csvs.save(file, folder=dest_folder)

                elif extension.lower() == '.xls' or extension.lower() == '.xlsx':
                    dir_path = os.path.join(app.config.get("UPLOADED_EXCEL_DEST"), dest_folder)
                    full_path = os.path.abspath(dir_path)
                    file.filename = "sap_export_file{0}{1}".format(analysis_date, extension.lower())
                    sap_export_file = file.filename
                    excel.save(file, folder=dest_folder)
                    # Check headers in SAP file names & count of headers ,If headers
                    # are valid then only save it.
                    check_header_sap_file(file, sap_export_file, full_path)

            sap_file = os.path.join(full_path, sap_export_file)

            prospect_id = add_prospect(args['user_email_id'])
            save_analysis_record_db()
            analysis_id = get_analysis_id()

            update_prospect_step(prospect_id, 1, analysis_date)  # Processing Files Status
            print("Prospect :'{0}' is at prospect_id: {1}".format(args['user_email_id'], prospect_id))

            #derive_table_creation(dna_file, sap_file, analysis_date, args['user_email_id'], analysis_id, customer_name, prospect_id, replenish_time)

            celery.send_task('app.tasks.derive_table_creation', [dna_file, sap_file, analysis_date,
                                                                args['user_email_id'], analysis_id,
                                                               customer_name, prospect_id, replenish_time],args['analysis_name'])

            return jsonify(msg="Files Uploaded Successfully", http_status_code=200, analysis_id=analysis_id)

        except FileFormatIssue as e:
            return jsonify(msg=e.msg, http_status_code=400)

        except Exception as e:
            print(str(e))
            return jsonify(msg="Error in File Uploading,Please try again", http_status_code=400)


class Reference(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('reference_name', required=True, location='form')
        self.reqparse.add_argument('reference_version', location='form')
        self.reqparse.add_argument('id', location='form')
        self.reqparse.add_argument('user_email_id', required=True, location='form')
        super(Reference, self).__init__()

    @requires_auth
    def post(self):
        print('hitted successfully')
        args = self.reqparse.parse_args()
        dest_folder = request.form.get('user_email_id')
        analysis_date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        reference_file = ''
       
        def update_reference_record_db():
            print('calling query')
            engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args)
            query = "UPDATE reference SET filename = '{0}', name= '{1}' WHERE id = {2}".format(reference_file,args['reference_name'],args['id'])
            print('query ---->',query)
            engine.execute(query)

        def save_reference_record_db():
            print('caling query')
            engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args)
            query = "INSERT INTO reference (name, version, isactive, " \
                    "filename, user_email_id,created_at,status) values ('{0}',{1},{2},'{3}','{4}'," \
                    "'{5}',{6})".format( args['reference_name'], reference_id+1,
                                                True,reference_file,
                                                args['user_email_id'], analysis_date,False)
            print('query ---->',query)
            engine.execute(query)

        def get_refernce_id():
            print('calling query')
            engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args)
            query = 'SELECT max(id) FROM reference;'
            result = engine.execute(query).fetchone()
            return result[0]

        try:
            print('request ----->',request.files.getlist('reference_file'))
            for file in request.files.getlist('reference_file'):
                extension = os.path.splitext(file.filename)
                if extension[1] == '.csv':
                    file.filename = "reference_file_{0}{1}".format(analysis_date, extension[1])
                    reference_file = file.filename
                    csvs.save(file, folder=dest_folder)

                elif extension[1] == '.xls' or extension == '.xlsx':
                    file.filename = "reference_file_{0}{1}".format(analysis_date, extension[1])
                    reference_file = file.filename
                    excel.save(file, folder=dest_folder)

            reference_id =  get_refernce_id()
            if reference_id == None :
                reference_id = 0
            print('id ----->',args['id'])
            if args['id'] == None :
                save_reference_record_db()
            else :
                update_reference_record_db()

            return jsonify(msg="Files Uploaded Successfully", http_status_code=200)
        except:
            return jsonify(msg="Error in File Uploading,Please try again", http_status_code=400)


class GetReference(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_email_id', type=str, required=True, help='id', location='args')
        super(GetReference, self).__init__()

    @requires_auth
    def get(self):
        args = self.reqparse.parse_args()
        user_email_id = args['user_email_id']
        query = "SELECT * FROM reference where user_email_id='{0}' AND status={1}".format(user_email_id,True)

        result = get_df_from_sql_query(
            query=query,
            db_connection_string=Configuration.INFINERA_DB_URL)

        response = json.loads(result.to_json(orient="records", date_format='iso'))
        return response


class DefaultReference(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('reference_id', type=int, required=True, help='id', location='args')
        self.reqparse.add_argument('user_email_id')
        super(DefaultReference, self).__init__()

    @requires_auth
    def post(self):
        args = self.reqparse.parse_args()
        reference_id = args['reference_id']
        user_email_id = args['user_email_id']
        try :
            references = "SELECT * from reference WHERE user_email_id='{0}'".format(user_email_id)
            print('references query ---->',references)
            result = get_df_from_sql_query(
            query=references,
            db_connection_string=Configuration.INFINERA_DB_URL)
            response = json.loads(result.to_json(orient="records", date_format='iso'))
            print('response ----->',response)
            engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args)

            for ref in response :
                print('ref ---->',ref)
                deactivatequery = "UPDATE reference SET isactive = {0} WHERE id = {1}".format(False,ref['id'])
                print('query ---->',deactivatequery)
                engine.execute(deactivatequery)
            
            activatequery = "UPDATE reference SET isactive = {0} WHERE id = {1}".format(True,reference_id)
            print('query ---->',activatequery)
            engine.execute(activatequery)
            return jsonify(msg="Updated Successfully", http_status_code=200)
        except:
            return jsonify(msg="Error in updating,Please try again", http_status_code=400)


class GetReferenceById(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('reference_id', type=int, required=True, help='id', location='args')
        super(GetReferenceById, self).__init__()

    @requires_auth
    def get(self):
        args = self.reqparse.parse_args()
        reference_id = args['reference_id']
        query = "SELECT * FROM reference where id={0}".format(reference_id)

        result = get_df_from_sql_query(
            query=query,
            db_connection_string=Configuration.INFINERA_DB_URL)

        response = json.loads(result.to_json(orient="records", date_format='iso'))
        return response

            




