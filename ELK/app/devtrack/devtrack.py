from flask import jsonify
from flask import request
import requests
from flask_restful import Resource
from flask_restful import reqparse

class DevTrackData(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('search_param', required=False, help='search_param', location='args')
        super(DevTrackData, self).__init__()

    def get(self):
        try:
            args = self.reqparse.parse_args()
           
            search_param = args['search_param']
            print(search_param)
            URL="http://54.191.115.241:9200/infinera/_search"
            headers = {'Content-type': 'application/json'}
            PARAMS = "{\"query\": {\"query_string\": {\"query\": \""+search_param+"\",\"fields\": [\"title\", \"severity\",\"description\",\"Found in Release\"]}}}"
            r = requests.get(url = URL, data = PARAMS, headers=headers) 
            data = r.json()
            return jsonify(data=data, http_status_code=200)
        except Exception as e:
            print(e)
            return jsonify(msg="Error in Updating,Please try again", http_status_code=400)
        