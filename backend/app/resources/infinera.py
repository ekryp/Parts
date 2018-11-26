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
from app.tasks import celery #, derive_table_creation

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
            dna_file = os.path.join(full_path, customer_dna_file)
            sap_file = os.path.join(full_path, sap_export_file)
            celery.send_task('app.tasks.derive_table_creation', [dna_file, sap_file, full_path])

            return jsonify(msg="Files Uploaded Successfully", http_status_code=200)
        except:
            return jsonify(msg="Error in File Uploading,Please try again", http_status_code=400)




