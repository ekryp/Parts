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


class FAQ(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title',  location='form')
        self.reqparse.add_argument('description', location='form')
        self.reqparse.add_argument('permissions', location='form')
        self.reqparse.add_argument('faq_id', location='form')
        super(FAQ, self).__init__()

    @requires_auth
    def patch(self):
        args = self.reqparse.parse_args()
        title = args['title']
        description = args['description']
        permissions = args['permissions']
        faq_id = args['faq_id']
        try:
            query = "update faq_details set title='{0}',description='{1}',permissions='{2}' where faq_id={3}".format(title,description,permissions,faq_id)
            engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args, echo=False)
            engine.execute(query)
            return jsonify(msg=" FAQ Details Updated Successfully", http_status_code=200)
        except:
            return jsonify(msg="Error in Updating,Please try again", http_status_code=400)

    @requires_auth
    def put(self):
        
        args = self.reqparse.parse_args()
        title = args['title']
        description = args['description']
        permissions = args['permissions']
        # bucketName = "infinera-data"
        # Key = ""
        # outPutname = "my_file"

        try:
            # for file in request.files.getlist('faq_image_file'):
            #     sqs = sqs_resource.meta.client
            #     s3 = boto3.client('s3', is_secure=False)
            #     res=s3.upload_file(file,bucketName,file.filename,extra_args={'ServerSideEncryption': "AES256"})
            #     print(res)
           
            engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args, echo=False)
            query="insert into faq_details (title,description,permissions) values('{0}','{1}','{2}')".format(title,description,permissions)
            engine.execute(query)
            return jsonify(msg="Inserted FAQ Details Successfully", http_status_code=200)
        except Exception as e:
            
            logging.error('...', exc_info=True)
            print('exception is ',e)
            return jsonify(msg="Error in Inserting,Please try again", http_status_code=400)

    @requires_auth
    def get(self):
        query = "SELECT faq_id,title,description,permissions FROM faq_details"

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
        faq_id = args['faq_id']
        try:
            query = "delete from faq_details where faq_id = {0}".format(faq_id)
            engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args, echo=False)

            result=engine.execute(query)
             #result = result.loc[:, ~result.columns.duplicated()]
             #Removes duplicate column names not column values
            
            return jsonify(msg=" FAQ Details Deleted Successfully", http_status_code=200)
        except:
            return jsonify(msg="Error in Deleting,Please try again", http_status_code=400)

    def options(self):
            return