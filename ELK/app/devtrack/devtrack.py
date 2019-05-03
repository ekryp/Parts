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

        def devtrack(search_param):
            URL="http://34.83.90.206:9200/devtrack/_search"
            headers = {'Content-type': 'application/json'}
            PARAMS = "{\"from\" : 0, \"size\" : 50,\"query\": {\"query_string\": {\"query\": \""+search_param+"\",\"fields\": [\"title\", \"severity\",\"description\",\"Found in Release\"]}}}"
            r = requests.get(url = URL, data = PARAMS, headers=headers) 
            data = r.json()
            devtrackmaxScore = data['hits']['max_score']
            devtrackList = data['hits']['hits']
            devTrack = []
            for doc in devtrackList:
                data = doc["_source"]
                data["probability"]= (doc["_score"]/devtrackmaxScore)*100
                devTrack.append(data)
            return devTrack
        
        def releaseNotes(search_param):
            URL="http://34.83.90.206:9200/release_notes/_search"
            headers = {'Content-type': 'application/json'}
            PARAMS = "{\"from\" : 0, \"size\" : 50,\"query\": {\"query_string\": {\"query\": \""+search_param+"\",\"fields\": [\"issueId\", \"severity\",\"description\",\"workaround\",\"file_name\"]}}}"
            r = requests.get(url = URL, data = PARAMS, headers=headers) 
            data = r.json()
            releaseNotesmaxScore = data['hits']['max_score']
            releaseNotesList = data['hits']['hits']
            releaseNotes = []
            for doc in releaseNotesList:
                data = doc["_source"]
                data["probability"]= (doc["_score"]/releaseNotesmaxScore)*100
                releaseNotes.append(data)
            return releaseNotes


        try:
            args = self.reqparse.parse_args()
           
            search_param = "*"+args['search_param']+"*"
            devTrack = devtrack(search_param)
            releaseNotes = releaseNotes(search_param)
            fsb = []
            response= {
                    "devTrack": [],
                    "releaseNotes": [],
                    "fsb": []
                }
            response['devTrack'] = devTrack
            response['releaseNotes'] = releaseNotes
            response['fsb'] = fsb
            
            return jsonify(data=response, http_status_code=200)
        except Exception as e:
            print(e)
            return jsonify(msg="Error in Fetching Data,Please try again", http_status_code=500)
        

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