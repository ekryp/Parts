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
        self.reqparse.add_argument('product_filter', required=False, location='args', action='append')
        self.reqparse.add_argument('group_filter', required=False, location='args', action='append')
        self.reqparse.add_argument('found_in_release_filter', required=False, location='args', action='append')
        self.reqparse.add_argument('fixed_in_release_filter', required=False, location='args', action='append')
        self.reqparse.add_argument('severity_filter', required=False, location='args', action='append')
        self.reqparse.add_argument('priority_filter', required=False, location='args', action='append')
        self.reqparse.add_argument('found_on_platform_filter', required=False, location='args', action='append')
        self.reqparse.add_argument('date_filter', required=False, location='args', action='append')
        super(DevTrackData, self).__init__()

    def get(self):

        def devtrack(search_param,product_filter,group_filter,found_in_release_filter,fixed_in_release_filter,severity_filter,priority_filter,found_on_platform_filter,date_filter):
            if not(isinstance(product_filter,list)):
                product_filter=[]
            if not(isinstance(group_filter,list)):
                group_filter=[]
            if not(isinstance(found_in_release_filter,list)):
                found_in_release_filter=[]
            if not(isinstance(fixed_in_release_filter,list)):
                fixed_in_release_filter=[]
            if not(isinstance(severity_filter,list)):
                severity_filter=[]
            if not(isinstance(priority_filter,list)):
                priority_filter=[]
            if not(isinstance(found_on_platform_filter,list)):
                found_on_platform_filter=[]
            if not(isinstance(date_filter,list)):
                date_filter=[]
            
            URL="http://34.83.90.206:9200/devtrack/_search"
            headers = {'Content-type': 'application/json'}
            if((len(product_filter)==0) and (len(group_filter)==0)and (len(found_in_release_filter)==0)and (len(fixed_in_release_filter)==0)and (len(severity_filter)==0)and (len(priority_filter)==0)and (len(found_on_platform_filter)==0)):
                PARAMS = "{\"from\" : 0, \"size\" : 50,\"query\": {\"query_string\": {\"query\": \""+search_param+"\",\"fields\": [\"title\", \"severity\",\"description\",\"Found in Release\"]}}}"
            else:
                PARAMS="{\"query\": {\"bool\": {\"should\": {\"query_string\": {\"query\": \""+search_param+"\"}},\"filter\": {\"bool\" : {\"must\" : ["

                if(len(product_filter)>0):
                    PRODUCT_PARAMS=""
                    PRODUCT_PARAMS+="{\"terms\" : { \"product\" : ["
                    for loc in product_filter:
                        if loc == product_filter[-1]:
                            PRODUCT_PARAMS+="\""+loc.lower()+"\"] } }"
                        else:
                            PRODUCT_PARAMS+="\""+loc.lower()+"\","

                if(len(group_filter)>0):
                    GROUP_PARAMS=""
                    GROUP_PARAMS+="{\"terms\" : { \"group\" : ["
                    for loc in group_filter:
                        if loc == group_filter[-1]:
                            GROUP_PARAMS+="\""+loc.lower()+"\"] } }"
                        else:
                            GROUP_PARAMS+="\""+loc.lower()+"\","


                if(len(found_in_release_filter)>0):
                    FOUND_IN_RELEASE_PARAMS=""
                    FOUND_IN_RELEASE_PARAMS+="{\"terms\" : { \"foundinRelease\" : ["
                    for loc in found_in_release_filter:
                        if loc == found_in_release_filter[-1]:
                            FOUND_IN_RELEASE_PARAMS+="\""+loc.lower()+"\"] } }"
                        else:
                            FOUND_IN_RELEASE_PARAMS+="\""+loc.lower()+"\","

                if(len(fixed_in_release_filter)>0):
                    FIXED_IN_RELEASE_PARAMS = ""
                    FIXED_IN_RELEASE_PARAMS+="{\"terms\" : { \"fixedinRelease\" : ["
                    for loc in fixed_in_release_filter:
                        if loc == fixed_in_release_filter[-1]:
                            FIXED_IN_RELEASE_PARAMS+="\""+loc.lower()+"\"] } }"
                        else:
                            FIXED_IN_RELEASE_PARAMS+="\""+loc.lower()+"\","

                if(len(severity_filter)>0):
                    SEVERITY_PARAMS = ""
                    SEVERITY_PARAMS+="{\"terms\" : { \"severity\" : ["
                    for loc in severity_filter:
                        if loc == severity_filter[-1]:
                            SEVERITY_PARAMS+="\""+loc.lower()+"\"] } }"
                        else:
                            SEVERITY_PARAMS+="\""+loc.lower()+"\","

             

                if(len(priority_filter)>0):
                    PRIORITY_PARAMS = ""
                    PRIORITY_PARAMS+="{\"terms\" : { \"priority\" : ["
                    for loc in priority_filter:
                        if loc == priority_filter[-1]:
                            PRIORITY_PARAMS+="\""+loc.lower()+"\"] } }"
                        else:
                            PRIORITY_PARAMS+="\""+loc.lower()+"\","


                if(len(found_on_platform_filter)>0):
                    FOUND_ON_PLATFORM_PARAMS=""
                    FOUND_ON_PLATFORM_PARAMS+="{\"terms\" : { \"foundOnPlatform\" : ["
                    for loc in found_on_platform_filter:
                        if loc == found_on_platform_filter[-1]:
                            FOUND_ON_PLATFORM_PARAMS+="\""+loc.lower()+"\"] } }"
                        else:
                            FOUND_ON_PLATFORM_PARAMS+="\""+loc.lower()+"\","

                if(len(date_filter)>0):
                    DATE_FILTER_PARAMS=""
                    DATE_FILTER_PARAMS+="{\"terms\" : { \"dateClosed\" : ["
                    for loc in date_filter:
                        if loc == date_filter[-1]:
                            DATE_FILTER_PARAMS+="\""+loc.lower()+"\"] } }"
                        else:
                            DATE_FILTER_PARAMS+="\""+loc.lower()+"\","

                
            
            if (len(product_filter)>0):
                PARAMS+=PRODUCT_PARAMS+","
                
            elif (len(group_filter)>0):
                PARAMS+=GROUP_PARAMS+","
                
            elif (len(found_in_release_filter)>0):
                PARAMS+=FOUND_IN_RELEASE_PARAMS+","
                
            elif (len(fixed_in_release_filter)>0):
                PARAMS+=FIXED_IN_RELEASE_PARAMS+","
                
            elif (len(severity_filter)>0):
                PARAMS+=SEVERITY_PARAMS+","
                
            elif (len(priority_filter)>0):
                PARAMS+=PRIORITY_PARAMS+","
                
            elif (len(found_on_platform_filter)>0):
                PARAMS+=FOUND_ON_PLATFORM_PARAMS+","
                
            elif (len(date_filter)>0):
                PARAMS+=DATE_FILTER_PARAMS+","
                

            if((len(product_filter)>0) or (len(group_filter)>0)or (len(found_in_release_filter)>0)or (len(fixed_in_release_filter)>0)or (len(severity_filter)>0)or (len(priority_filter)>0)or (len(found_on_platform_filter)>0)):
                PARAMS = PARAMS[:-1]
                PARAMS+="]}}}}}"
            print(PARAMS)
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

        def fsb(search_param):
            URL="http://34.83.90.206:9200/fsb/_search"
            headers = {'Content-type': 'application/json'}
            PARAMS = "{\"from\" : 0, \"size\" : 50,\"query\": {\"query_string\": {\"query\": \""+search_param+"\",\"fields\": [\"issueId\", \"title\",\"description\",\"symptoms\",\"rootCause\", \"file_name\",\"FSBNumber\",\"dateCreated\",\"dateRevised\"]}}}"
            r = requests.get(url = URL, data = PARAMS, headers=headers) 
            data = r.json()
            fsbmaxScore = data['hits']['max_score']
            fsbList = data['hits']['hits']
            fsb = []
            for doc in fsbList:
                data = doc["_source"]
                data["probability"]= (doc["_score"]/fsbmaxScore)*100
                fsb.append(data)
            return fsb


        try:
            args = self.reqparse.parse_args()
           
            search_param = "*"+args['search_param']+"*"
            product_filter = args.get('product_filter')
            group_filter = args.get('group_filter')
            found_in_release_filter = args.get('found_in_release_filter')
            fixed_in_release_filter = args.get('fixed_in_release_filter')
            severity_filter = args.get('severity_filter')
            priority_filter = args.get('priority_filter')
            found_on_platform_filter = args.get('found_on_platform_filter')
            date_filter = args.get('date_filter')
            date_filter
            devTrack = devtrack(search_param,product_filter,group_filter,found_in_release_filter,fixed_in_release_filter,severity_filter,priority_filter,found_on_platform_filter,date_filter)
            releaseNotes = releaseNotes(search_param)
            fsb = fsb(search_param)
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
