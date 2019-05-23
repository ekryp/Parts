from flask import jsonify
from flask import request
import requests
import re
import config
from requests.auth import HTTPBasicAuth
from flask_restful import Resource
from flask_restful import reqparse
import csv, json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from elasticsearch import Elasticsearch
import logging

from flask import jsonify
from flask import request
import requests
from flask_restful import Resource
from flask_restful import reqparse
import pandas as pd

class ReleaseNotes(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('search_param', required=False, location='args')
        self.reqparse.add_argument('data',required=False,help='data',location='form')
        super(ReleaseNotes, self).__init__()

    def put(self):
        try:
            args = self.reqparse.parse_args()
            
            data = args['data']
            doc=json.loads(data)
            response = requests.put(config.ELK_URI+"release_notes/_doc/"+doc["key"],json=doc,auth=HTTPBasicAuth(config.ELK_USERNAME,config.ELK_PASSWORD),headers={"content-type":"application/json"})
            return jsonify(msg=response.json(),http_status_code=200)
        except Exception as e:
            print(e)
            return jsonify(msg="Error in Fetching Data,Please try again", http_status_code=400)

    def get(self):
        search_param = "*"+args['search_param']+"*"
        search_param=re.sub('[^A-Za-z0-9*. ]+', '', search_param)
    
    def options(self):
         pass