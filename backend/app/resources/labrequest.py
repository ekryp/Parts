import json
import os
from datetime import datetime
from app.auth.authorization import requires_auth
import pandas as pd
from app import Configuration
from app import app
from app import csvs, excel, mytext, my_tsvs
from app.tasks import celery, add_prospect, update_prospect_step
from app.utils.utils import get_df_from_sql_query
from flask import jsonify
from flask import request
from flask_restful import Resource
from flask_restful import reqparse
from sqlalchemy import create_engine
import pytz


class PostLabRequest(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', required=True, location='form')
        self.reqparse.add_argument('lab_resource', required=True, location='form')
        self.reqparse.add_argument('requested_date', required=True, location='form')
        self.reqparse.add_argument('start_time', required=True, location='form')
        self.reqparse.add_argument('end_time', required=True, location='form')
        self.reqparse.add_argument('type', required=True, location='form')
        self.reqparse.add_argument('description', required=False, location='form')
        self.reqparse.add_argument('created_by', required=True, location='form')
        super(PostLabRequest, self).__init__()

    
    @requires_auth
    def post(self):
        args = self.reqparse.parse_args()
        initial_status = 'pending_request'
        utc = pytz.utc
        args['created_at'] = datetime.now(tz=utc)
        try:
            
            engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args)
            query = "INSERT into lab_request (title, lab_resource, requested_date, start_time, end_time, type, description, status, created_at, created_by) values ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}','{9}')".format(args['title'],args['lab_resource'],args['requested_date'],args['start_time'],args['end_time'],args['type'],args['description'],initial_status,args['created_at'],args['created_by'])
            engine.execute(query)
            return jsonify(msg="Lab Request Created Successfully", http_status_code=200)
        except Exception as e:
            print(str(e))
            return jsonify(msg="Error in Creating Lab Request", http_status_code=500)

class GetAllLabRequest(Resource):

    @requires_auth
    def get(self):
        try:
            query = "SELECT * FROM lab_request"
            data = get_df_from_sql_query(query=query,
            db_connection_string=Configuration.INFINERA_DB_URL)
            response = json.loads(data.to_json(orient="records", date_format='iso'))
            return jsonify(msg="GetAll Lab Request Successfully", http_status_code=200, data=response)
        except Exception as e:
            print(str(e))
            return jsonify(msg="Error in GetAll Lab Request", http_status_code=500)

        
