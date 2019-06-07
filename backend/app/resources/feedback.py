from app import app
from app import csvs, excel, mytext,images
from flask import jsonify
from flask import request
from sqlalchemy import create_engine, exc
from flask_restful import Resource
from app.tasks import sendEmailNotificatio
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


class Feedback(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title',  location='form')
        self.reqparse.add_argument('feedback', location='form')
        super(Feedback, self).__init__()

  

    @requires_auth
    def put(self):
        
        args = self.reqparse.parse_args()
        title = args['title']
        feedback = args['feedback']
        

        try:
            subject=' Feedback Notification '
            message= title+'\n'+feedback
            email_response=sendEmailNotificatio('nageshwara.vijay@ekryp.com', subject, message)
            engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args, echo=False)
            query="insert into feedback (title,feedback) values('{0}','{1}')".format(title,feedback)
            engine.execute(query)
            return jsonify(msg="Inserted Feedback Details Successfully", http_status_code=200)
        except Exception as e:
            
            logging.error('...', exc_info=True)
            print('exception is ',e)
            return jsonify(msg="Error in Inserting,Please try again", http_status_code=400)

   
    def options(self):
            return