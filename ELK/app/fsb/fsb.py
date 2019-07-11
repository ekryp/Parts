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
from app.common import escapeESArg
from app.auth.authorization import requires_auth
from flask import request
import requests
from flask_restful import Resource
from flask_restful import reqparse
import pandas as pd

class FSB(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('search_param', required=False, location='args')
        self.reqparse.add_argument('data',required=False,help='data',location='form')
        super(FSB, self).__init__()
    @requires_auth
    def put(self):
        try:
            args = self.reqparse.parse_args()
            
            data = args['data']
            doc=json.loads(data)
            response = requests.put(config.ELK_URI+"fsb/_doc/"+doc["key"],json=doc,auth=HTTPBasicAuth(config.ELK_USERNAME,config.ELK_PASSWORD),headers={"content-type":"application/json"})
            return jsonify(msg=response.json(),http_status_code=200)
        except Exception as e:
            print(e)
            return jsonify(msg="Error in Fetching Data,Please try again", http_status_code=400)
    @requires_auth
    def get(self):
        args = self.reqparse.parse_args()
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        search_param = escapeESArg(args['search_param'])
        splited_search_param = search_param.split(' ')
        updated_search_param = splited_search_param[0]
        for tmp in splited_search_param[1:]:
            updated_search_param += " AND "+tmp
        search_param = updated_search_param
        print(search_param)
        print("FSB  Params : ", search_param)
        es = Elasticsearch(config.ELK_URI, http_auth=(config.ELK_USERNAME,config.ELK_PASSWORD))
        if (search_param != ""):
            data = es.search(index="fsb", body={"from" : 0, "size" : 10000,"query": {"query_string": {"query": search_param,"fields": ["issueId", "title","description","symptoms","rootCause", "file_name","FSBNumber","dateCreated","dateRevised"]}}})
        else:
            # data = requests.get(config.ELK_URI+"testplan/_doc/_search",auth=HTTPBasicAuth(config.ELK_USERNAME,config.ELK_PASSWORD),headers={"content-type":"application/json"})
            # data = data.json()
            data = es.search(index="fsb", body={"from" : 0, "size" : 10000,"query": { "match_all": {}}})
        
        fsbmaxScore = data['hits']['max_score']
        fsbList = data['hits']['hits']
        fsb = []

        for doc in fsbList:
            data = doc["_source"]
            data['key']=doc['_id']
            data["probability"]= round((doc["_score"]/fsbmaxScore)*100)
            fsb.append(data)
        response = {"fsb": [] }

        response['fsb'] = fsb
        return jsonify(data=response, http_status_code=200)


    
    def options(self):
         pass