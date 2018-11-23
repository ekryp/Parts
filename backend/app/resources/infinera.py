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
        #self.reqparse.add_argument('analysis_time', required=True, location='form')
        self.reqparse.add_argument('analysis_type', required=True, location='form')
        self.reqparse.add_argument('replenish_time', required=True, location='form')
        #self.reqparse.add_argument('file_names', required=True, location='form')
        self.reqparse.add_argument('user_email_id', required=True, location='form')
        super(PostSparePartAnalysis, self).__init__()


    def post(self):
        args = self.reqparse.parse_args()
        dest_folder = request.form.get('user_email_id')
        analysis_date = str(datetime.now())
        for file in request.files.getlist('customer_dna_file'):

            name, extension = os.path.splitext(file.filename)

            if extension.lower() == '.csv':
                dir_path = os.path.join(app.config.get("UPLOADED_CSV_DEST"), dest_folder)
                full_path = os.path.abspath(dir_path)
                file.filename = "customer_dna_file_{0}{1}".format(analysis_date, extension.lower())
                csvs.save(file, folder=dest_folder)

            elif extension.lower() == '.xls' or extension == '.xlsx':
                dir_path = os.path.join(app.config.get("UPLOADED_EXCEL_DEST"), dest_folder)
                full_path = os.path.abspath(dir_path)
                file.filename = "customer_dna_file_{0}{1}".format(analysis_date, extension.lower())
                excel.save(file, folder=dest_folder)

        for file in request.files.getlist('sap_export_file'):

            name, extension = os.path.splitext(file.filename)

            if extension.lower() == '.csv':
                dir_path = os.path.join(app.config.get("UPLOADED_CSV_DEST"), dest_folder)
                full_path = os.path.abspath(dir_path)
                file.filename = "sap_export_file{0}{1}".format(analysis_date, extension.lower())
                csvs.save(file, folder=dest_folder)

            elif extension.lower() == '.xls' or extension.lower() == '.xlsx':
                dir_path = os.path.join(app.config.get("UPLOADED_EXCEL_DEST"), dest_folder)
                full_path = os.path.abspath(dir_path)
                file.filename = "sap_export_file{0}{1}".format(analysis_date, extension.lower())
                excel.save(file, folder=dest_folder)