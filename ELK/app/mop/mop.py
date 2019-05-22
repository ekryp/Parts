import config
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from flask import jsonify
import requests
from flask_restful import Resource
from flask_restful import reqparse
from elasticsearch import Elasticsearch


class MOP(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('search_param', required=False, location='args')
        self.reqparse.add_argument('data', required=False, help='data', location='form')
        super(MOP, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        if args['search_param']:
            search_param = "*" + args['search_param'] + "*"
            print(search_param)
        else:
            search_param = ""
        es = Elasticsearch(config.ELK_URI, http_auth=(config.ELK_USERNAME, config.ELK_PASSWORD))
        if search_param != "":
            data = es.search(index="mop", body={"from": 0, "size": 100, "query": {
                "query_string": {"query": search_param.lower(), "fields": ["file_name", "title", "introduction"]}}})
        else:
            data = es.search(index="mop", body={"from": 0, "size": 100, "query": {"match_all": {}}})
        mop_max_score = data['hits']['max_score']
        mop_list = data['hits']['hits']
        mop = []

        for doc in mop_list:
            data = doc["_source"]
            data['key'] = doc['_id']
            data["probability"] = round((doc["_score"] / mop_max_score) * 100)
            mop.append(data)
        response = {"mop": [] }

        response['mop'] = mop
        return jsonify(data=response, http_status_code=200)

    def options(self):
        pass
