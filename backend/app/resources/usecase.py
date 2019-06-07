from app import app
from app import csvs, excel, mytext,images
from flask import jsonify
from flask import request
from sqlalchemy import create_engine, exc
from flask_restful import Resource
from flask_restful import reqparse
from app.utils.utils import get_df_from_sql_query
import pandas as pd
import pdb
import os
import logging
import boto3
import json
from app import Configuration
from app.auth.authorization import requires_auth


class Usecase(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('usecase',  location='form')
        self.reqparse.add_argument('brief_description', location='form')
        self.reqparse.add_argument('description', location='form')
        self.reqparse.add_argument('ekryp_usecase_id', location='form')
        super(Usecase, self).__init__()

    @requires_auth
    def patch(self):
        args = self.reqparse.parse_args()
        usecase = args['usecase']
        description = args['description']
        brief_description = args['brief_description']
        ekryp_usecase_id = args['ekryp_usecase_id']
        try:
            query = "update ekryp_usecase set usecase='{0}',description='{1}',brief_description='{2}' ekryp_usecase_id faq_id={3}".format(usecase,description,brief_description,ekryp_usecase_id)
            engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args, echo=False)
            engine.execute(query)
            return jsonify(msg=" Usecase Details Updated Successfully", http_status_code=200)
        except:
            return jsonify(msg="Error in Updating,Please try again", http_status_code=400)

    @requires_auth
    def put(self):
        
        args = self.reqparse.parse_args()
        usecase = args['usecase']
        description = args['description']
        brief_description = args['brief_description']
       

        try:
           
           
            engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args, echo=False)
            query="insert into ekryp_usecase (usecase,description,brief_description) values('{0}','{1}','{2}')".format(usecase,description,brief_description)
            engine.execute(query)
            return jsonify(msg="Inserted Usecase Details Successfully", http_status_code=200)
        except Exception as e:
            
            logging.error('...', exc_info=True)
            print('exception is ',e)
            return jsonify(msg="Error in Inserting,Please try again", http_status_code=400)

    @requires_auth
    def get(self):
        query = "SELECT ekryp_usecase_id,usecase,description,brief_description FROM ekryp_usecase"

        result = get_df_from_sql_query(
            query=query,
            db_connection_string=Configuration.INFINERA_DB_URL)

        result = result.loc[:, ~result.columns.duplicated()]
         #Removes duplicate column names not column values
        response = json.loads(result.to_json(orient="records", date_format='iso'))
        return response

    @requires_auth
    def delete(self):
        args = self.reqparse.parse_args()
        ekryp_usecase_id = args['ekryp_usecase_id']
        try:
            query = "delete from ekryp_usecase where ekryp_usecase_id = {0}".format(faq_id)
            engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args, echo=False)

            result=engine.execute(query)
             #result = result.loc[:, ~result.columns.duplicated()]
             #Removes duplicate column names not column values
            
            return jsonify(msg=" Usecase Details Deleted Successfully", http_status_code=200)
        except:
            return jsonify(msg="Error in Deleting,Please try again", http_status_code=400)

    def options(self):
            return