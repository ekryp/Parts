import requests
from flask_restful import Resource
from flask_restful import reqparse
import json
import os
import sys
import requests
from flask import jsonify
import glob

from app import Configuration
from app.auth.authorization import requires_auth
from app.models.basemodel import get_session
from app.models.ekryp_user import User, UserSettings
import time, calendar
from sqlalchemy import create_engine
import pandas as pd
import traceback
from datetime import datetime, timedelta
from flask import _app_ctx_stack, session, request
import json
import time
import urllib
from app import app
from app import csvs,excel
from app.tasks import celery, add_prospect, update_prospect_step,derive_table_creation
from app.utils.utils import get_df_from_sql_query

class GetSparePartAnalysis(Resource):

    def get(self):
        engine = create_engine(Configuration.INFINERA_DB_URL)
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
        self.reqparse.add_argument('request_id', type=int, required=False, help='id', location='args')
        super(GetstepsforSpecificRequest, self).__init__()

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
        self.reqparse.add_argument('request_id', type=int, required=False, help='id', location='args')
        super(GetSummaryforSpecificRequest, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        request_id = args['request_id']
        query = "select PON,material_number,Qty, standard_cost,`gross table count`,`extd std cost`," \
                "`net depot count`,`net extd std cost`,`High Spares?`,a.user_email_id," \
                "a.analysis_request_time,analysis_request_id,analysis_name,customer_name" \
                " from summary_output as a " \
                "right join analysis_request as b on " \
                "a.analysis_request_time = b.analysis_request_time " \
                "and a.user_email_id = b.user_email_id where b.requestStatus='Completed' " \
                "and analysis_request_id = {0}".format(request_id)

        result = get_df_from_sql_query(
            query=query,
            db_connection_string=Configuration.INFINERA_DB_URL)

        result.rename(columns={
            "High Spares?": "High_Spares",
            "extd std cost": "extd_std_cost",
            "gross table count": "gross_table_count",
            "net depot count": "net_depot_count",
            "net extd std cost": "net_extd_std_cost",
        }, inplace=True
        )

        response = json.loads(result.to_json(orient="records", date_format='iso'))
        return response

class GetDashboardRequestCount(Resource):

    def get(self):

        def get_respective_counts():
            engine = create_engine(Configuration.INFINERA_DB_URL)

            total_request_query = "select count(*) from analysis_request"
            total_request = engine.execute(total_request_query).fetchone()[0]
            incomplete_request_query = "select count(*) from analysis_request where requestStatus = 'Processing'"
            incomplete_request = engine.execute(incomplete_request_query).fetchone()[0]
            complete_request_query = "select count(*) from analysis_request where requestStatus = 'Completed'"
            complete_request = engine.execute(complete_request_query).fetchone()[0]
            failed_request = 0
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


class PostSparePartAnalysis(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('analysis_name', required=True, location='form')
        self.reqparse.add_argument('analysis_type', required=True, location='form')
        self.reqparse.add_argument('replenish_time', required=True, location='form')
        self.reqparse.add_argument('customer_name', required=True, location='form')
        self.reqparse.add_argument('user_email_id', required=True, location='form')
        super(PostSparePartAnalysis, self).__init__()


    def post(self):
        args = self.reqparse.parse_args()
        dest_folder = request.form.get('user_email_id')
        analysis_date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        customer_dna_file = ''
        sap_export_file = ''

        def save_analysis_record_db():
            engine = create_engine(Configuration.INFINERA_DB_URL)
            query = "INSERT INTO analysis_request (cust_id, analysis_name, analysis_type, " \
                    "replenish_time, user_email_id, analysis_request_time, dna_file_name, " \
                    "sap_file_name, customer_name) values ({0},'{1}','{2}','{3}','{4}','{5}'," \
                    "'{6}','{7}','{8}')".format(7, args['analysis_name'], args['analysis_type'],
                                                args['replenish_time'].replace(",", "|"),
                                                args['user_email_id'], analysis_date,
                                                customer_dna_file, sap_export_file,
                                                args['customer_name'].replace(",", "|"))
            engine.execute(query)
        try:

            for file in request.files.getlist('customer_dna_file'):

                name, extension = os.path.splitext(file.filename)

                if extension.lower() == '.csv':
                    dir_path = os.path.join(app.config.get("UPLOADED_CSV_DEST"), dest_folder)
                    full_path = os.path.abspath(dir_path)
                    file.filename = "customer_dna_file_{0}{1}".format(analysis_date, extension.lower())
                    customer_dna_file = file.filename
                    csvs.save(file, folder=dest_folder)

                elif extension.lower() == '.xls' or extension == '.xlsx':
                    dir_path = os.path.join(app.config.get("UPLOADED_EXCEL_DEST"), dest_folder)
                    full_path = os.path.abspath(dir_path)
                    file.filename = "customer_dna_file_{0}{1}".format(analysis_date, extension.lower())
                    customer_dna_file = file.filename
                    excel.save(file, folder=dest_folder)

            for file in request.files.getlist('sap_export_file'):

                name, extension = os.path.splitext(file.filename)

                if extension.lower() == '.csv':
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

            save_analysis_record_db()

            prospect_id = add_prospect(args['user_email_id'])
            dna_file = os.path.join(full_path, customer_dna_file)
            sap_file = os.path.join(full_path, sap_export_file)
            #derive_table_creation(dna_file, sap_file, full_path, prospect_id, analysis_date, args['user_email_id'])

            print("Prospect :'{0}' is at prospect_id: {1}".format(args['user_email_id'], prospect_id ))
            '''
            update_prospect_step(prospect_id, 1, analysis_date)
            update_prospect_step(prospect_id, 2, analysis_date)
            update_prospect_step(prospect_id, 3, analysis_date)
            update_prospect_step(prospect_id, 4, analysis_date)
            '''
            celery.send_task('app.tasks.derive_table_creation', [dna_file, sap_file, full_path, prospect_id,
                                                                analysis_date, args['user_email_id']])


            return jsonify(msg="Files Uploaded Successfully", http_status_code=200)
        except:
            return jsonify(msg="Error in File Uploading,Please try again", http_status_code=400)




