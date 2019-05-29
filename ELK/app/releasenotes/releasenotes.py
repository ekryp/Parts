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
from app.common import escapeESArg
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
        args = self.reqparse.parse_args()
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        search_param = escapeESArg(args['search_param'])
        splited_search_param = search_param.split(' ')
        updated_search_param = splited_search_param[0]
        for tmp in splited_search_param[1:]:
            updated_search_param += " AND "+tmp
        search_param = updated_search_param
        print(search_param)
        print("Release Notes  Params : ", search_param)
        es = Elasticsearch(config.ELK_URI, http_auth=(config.ELK_USERNAME,config.ELK_PASSWORD))

        if (search_param != ""):
            data = es.search(index="release_notes", body={"from" : 0, "size" : 800,"query": {"query_string": {"query": search_param ,"fields": ["issueId", "severity","description","workaround","file_name"]}}})
        else:
            # data = requests.get(config.ELK_URI+"testplan/_doc/_search",auth=HTTPBasicAuth(config.ELK_USERNAME,config.ELK_PASSWORD),headers={"content-type":"application/json"})
            # data = data.json()
            data = es.search(index="release_notes", body={"from" : 0, "size" : 800,"query": { "match_all": {}}})
        
        releaseNotesmaxScore = data['hits']['max_score']
        releaseNotesList = data['hits']['hits']
        
        releaseNotes = []
        for doc in releaseNotesList:
            data = doc["_source"]
            data['key']=doc['_id'] 
            data["probability"]= round((doc["_score"]/releaseNotesmaxScore)*100)
            releaseNotes.append(data)
        response = {"releaseNotes": [] }

        response['releaseNotes'] = releaseNotes
        return jsonify(data=response, http_status_code=200)



    def options(self):
         pass