import config
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from flask import jsonify
import requests
from flask_restful import Resource
import json
import re
from requests.auth import HTTPBasicAuth
from flask_restful import reqparse
from elasticsearch import Elasticsearch
from app.common import escapeESArg


class TechNotes(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('search_param', required=False, location='args')
        self.reqparse.add_argument('data', required=False, help='data', location='form')
        self.reqparse.add_argument('phrase_query', required=False, location='args', action='append')
        self.reqparse.add_argument('predict_value', required=False, help='predict_value', location='args')
        super(TechNotes, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        phrase_query= args['phrase_query']
        predict_value = args['predict_value']
        search_param = args['search_param']
        search_param = escapeESArg(search_param)
        search_param=re.sub(' +', ' ', search_param)
        print('search Param',search_param)
        print('phrase_query Param',phrase_query)
        print('predict_value Param',predict_value)
        print('type of test plan predict val',type(predict_value))
        final_list=[]
        if predict_value is not None:
            predict_value_list=predict_value.split(",")
        
            if (len(predict_value_list)>0):
                predict_value_list.pop(0)
                for predict_list in predict_value_list:
                        filter_list=[]
                        for tmp in predict_list.split('|')[1:]:
                            filter_list.append(tmp)
                        final_list.append(filter_list)    
        print('filter list ',final_list)
        if not(isinstance(phrase_query,list)):
            phrase_query=[]
        search_param_list = search_param.split(' ')
        if(len(phrase_query)>0):
            for phrase in phrase_query:
                search_param_list.append(phrase)
        search_param_list = list( dict.fromkeys(search_param_list)) 

        PARAMS="{\"from\" : 0, \"size\" : 100,\"query\": {\"bool\": {\"must\": ["
                        
        if(len(search_param_list)>0):
            for tmp in search_param_list:
                
                
                if not(tmp == ""):
                    if tmp == search_param_list[-1]:
                        PARAMS+="{\"multi_match\": {\"query\": \""+tmp+"\",\"type\" : \"phrase_prefix\"}},"
                    else:
                        PARAMS+="{\"multi_match\": {\"query\": \""+tmp+"\",\"type\" : \"phrase_prefix\"}},"

        if(len(final_list)>0):
            
            for tmp_list in final_list:
                PARAMS+=" {\"bool\": {\"should\": ["
                for tmp in tmp_list:
                    
                    if not(tmp == ""):
                        if tmp == tmp_list[-1]:
                            PARAMS+="{\"multi_match\": {\"query\": \""+tmp+"\",\"type\" : \"phrase_prefix\"}}"
                        else:
                            PARAMS+="{\"multi_match\": {\"query\": \""+tmp+"\",\"type\" : \"phrase_prefix\"}},"
                PARAMS+="]}},"
        
        PARAMS=PARAMS[:-1]
        PARAMS+="]}}}"
        print('Query Used',PARAMS)
        print('length',len(search_param_list))
        es = Elasticsearch(config.ELK_URI, http_auth=(config.ELK_USERNAME,config.ELK_PASSWORD))
        data = es.search(index="technotes", body=json.loads(PARAMS))
        technotes_max_score = data['hits']['max_score']
        technotes_list = data['hits']['hits']
        technotes = []

        for doc in technotes_list:
            data = doc["_source"]
            data['key'] = doc['_id']
            data["probability"] = round((doc["_score"] / technotes_max_score) * 100)
            technotes.append(data)
        response = {"technotes": []}
        response['technotes'] = technotes
        return jsonify(data=response, http_status_code=200)

    def put(self):
        try:
            args = self.reqparse.parse_args()
            data = args['data']
            doc = json.loads(data)
            response = requests.put(config.ELK_URI + "technotes/_doc/" + doc["key"], json=doc,
                                    auth=HTTPBasicAuth(config.ELK_USERNAME, config.ELK_PASSWORD),
                                    headers={"content-type": "application/json"})
            return jsonify(msg=response.json(), http_status_code=200)
        except Exception as e:
            print(e)
            return jsonify(msg="Error in Fetching Data,Please try again", http_status_code=400)

    def options(self):
        pass
