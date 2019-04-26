from flask import jsonify
from flask import request
import requests
from flask_restful import Resource
from flask_restful import reqparse
import csv, json

class DevTrackData(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('search_param', required=False, help='search_param', location='args')
        self.reqparse.add_argument('issue_id',required=False,help='issue_id',location='args')
        self.reqparse.add_argument('data',required=False,help='data',location='form')
        super(DevTrackData, self).__init__()

    def get(self):

        try:
            args = self.reqparse.parse_args()
           
            search_param = args['search_param']
            print(search_param)
            URL="http://54.191.115.241:9200/infinera/_search"
            headers = {'Content-type': 'application/json'}
            PARAMS = "{\"from\" : 0, \"size\" : 50,\"query\": {\"query_string\": {\"query\": \""+search_param+"\",\"fields\": [\"title\", \"severity\",\"description\",\"Found in Release\"]}}}"
            r = requests.get(url = URL, data = PARAMS, headers=headers) 
            data = r.json()
            esResponses = data['hits']['hits']
            devTrack = []
            releaseNotes = []
            salesForces = []
            response= {
                    "totalhits": data['hits']['total']['value'],
                    "devTrack": [],
                    "releaseNotes": [],
                    "salesForces": []
                }
            for doc in esResponses:
                data = doc["_source"]
                if(doc["_type"] == "devtrack"):
                    data["probability"]= doc["_score"]
                    devTrack.append(data)
                if(doc["_type"] == "releasenotes"):
                    data["probability"]= doc["_score"]
                    releaseNotes.append(data)
                if(doc["_type"] == "salesforce"):
                    data["probability"]= doc["_score"]
                    salesForces.append(data)
            response['devTrack'] = devTrack
            response['releaseNotes'] = releaseNotes
            response['salesForces'] = salesForces
            
            return jsonify(data=response, http_status_code=200)
        except Exception as e:
            print(e)
            return jsonify(msg="Error in Fetching Data,Please try again", http_status_code=400)
        

    def put(self):
        try:
            args = self.reqparse.parse_args()
            issue_id = args['issue_id']
            data = args['data']
            doc=json.loads(data)
            
            response = requests.put("http://54.191.115.241:9200/infinera/devtrack/"+doc["issueId"],json=doc,headers={"content-type":"application/json"})
            print(response)
            return jsonify(msg=response.json(),http_status_code=200)
        except Exception as e:
            print(e)
            return jsonify(msg="Error in Fetching Data,Please try again", http_status_code=400)

    
    def options(self):
         pass