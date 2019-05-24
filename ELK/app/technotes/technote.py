import config
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from flask import jsonify
import requests
from flask_restful import Resource
import json
from requests.auth import HTTPBasicAuth
from flask_restful import reqparse
from elasticsearch import Elasticsearch
from app.common import escapeESArg


class TechNotes(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('search_param', required=False, location='args')
        self.reqparse.add_argument('data', required=False, help='data', location='form')
        super(TechNotes, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        if args['search_param']:
            search_param = escapeESArg(args['search_param'])
            search_param = "*" + search_param + "*"
            print(search_param)
        else:
            search_param = ""
        es = Elasticsearch(config.ELK_URI, http_auth=(config.ELK_USERNAME, config.ELK_PASSWORD))
        if search_param != "":
            data = es.search(index="technotes", body={"from": 0, "size": 100, "query": {
                "query_string": {"query": search_param.lower(), "fields": ["file_name", "release_product_affected", "description"]}}})
        else:
            data = es.search(index="technotes", body={"from": 0, "size": 100, "query": {"match_all": {}}})
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
