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


class TestPlan(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('search_param', required=True, location='args')
        self.reqparse.add_argument('data',required=False,help='data',location='form')
        super(TestPlan, self).__init__()

    def put(self):

        try:
            args = self.reqparse.parse_args()
            data = args['data']
            doc=json.loads(data)
            response = requests.put(config.ELK_URI+"testplan/_doc/"+doc["_id"],json=doc,auth=HTTPBasicAuth(config.ELK_USERNAME,config.ELK_PASSWORD),headers={"content-type":"application/json"})
            return jsonify(msg=response.json(),http_status_code=200)
        except Exception as e:
            print(e)
            return jsonify(msg="Error in Fetching Data,Please try again", http_status_code=400)
            
    def get(self):
        args = self.reqparse.parse_args()
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        search_param = args['search_param']
        search_param=search_param.lower()
        if (search_param == ""):
            search_param = "*"
        print(search_param)
        es = Elasticsearch(config.ELK_URI, http_auth=(config.ELK_USERNAME,config.ELK_PASSWORD))
        data = es.search(index="testplan", body={"from" : 0, "size" : 50,"query": {"query_string": {"query": search_param,"fields": ["file_name", "Objective","Procedure"]}}})
        test_max_score = data['hits']['max_score']
        test_plan_list = data['hits']['hits']
        test_plan = []

        for doc in test_plan_list:
            data = doc["_source"]
            data["probability"]= round((doc["_score"]/test_max_score)*100)
            test_plan.append(data)
        response= {
                    "test_plan": []
                }
            
        response['test_plan'] = test_plan
        return jsonify(data=response, http_status_code=200)

    
    def options(self):
         pass
