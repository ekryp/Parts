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
        self.reqparse.add_argument('check_title',required=False,help='check_title',location='args')
        self.reqparse.add_argument('internal', required=False, location='args')
        super(DevTrackData, self).__init__()

    def get(self):

        def devtrack(search_param,product_filter,group_filter,found_in_release_filter,fixed_in_release_filter,severity_filter,priority_filter,found_on_platform_filter,date_filter,checkTitle):
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

            DATE_FILTER_PARAMS=""
            
            URL=config.ELK_URI+"devtrack/_doc/_search"
            headers = {'Content-type': 'application/json'}
            if((len(product_filter)==0) and (len(group_filter)==0)and (len(found_in_release_filter)==0)and (len(fixed_in_release_filter)==0)and (len(severity_filter)==0)and (len(priority_filter)==0)and (len(found_on_platform_filter)==0)and (len(date_filter)==0)):
                print(check_title)
                if(check_title == "true"):
                    PARAMS = "{\"from\" : 0, \"size\" : 50,\"query\": {\"query_string\": {\"query\": \""+search_param+"\",\"fields\": [\"title\"]}}}"
                else:
                    PARAMS = "{\"from\" : 0, \"size\" : 50,\"query\": {\"query_string\": {\"query\": \""+search_param+"\",\"fields\": [ \"severity\",\"description\",\"foundinRelease\",\"issueId\"]}}}"

            else:
                if(check_title == "true"):
                    PARAMS="{\"from\" : 0, \"size\" : 50,\"query\": {\"bool\": {\"must\": {\"query_string\": {\"query\": \""+search_param+"\",\"fields\": [\"title\"]}},\"filter\": {\"bool\" : {\"must\" : ["
                else:
                    PARAMS="{\"from\" : 0, \"size\" : 50,\"query\": {\"bool\": {\"must\": {\"query_string\": {\"query\": \""+search_param+"\"}},\"filter\": {\"bool\" : {\"must\" : ["
                if(len(product_filter)>0):
                    PRODUCT_PARAMS=""
                    
                    for loc in product_filter:
                        if loc == product_filter[-1]:
                            PRODUCT_PARAMS+="{\"term\" : { \"product\" :\""+loc.lower()+"\" } }"
                        else:
                            PRODUCT_PARAMS+="{\"term\" : { \"product\" :\""+loc.lower()+"\"} },"

                if(len(group_filter)>0):
                    GROUP_PARAMS=""
                    for loc in group_filter:
                        for tmp in loc.split():
                            tmp=re.sub('[^A-Za-z0-9]+', '', tmp)
                            if not(tmp == ""):
                                if tmp == loc.split()[-1]:
                                    GROUP_PARAMS+="{\"term\" : { \"group\" :\""+tmp.lower()+"\" } }"
                                else:
                                    GROUP_PARAMS+="{\"term\" : { \"group\" :\""+tmp.lower()+"\"} },"


                if(len(found_in_release_filter)>0):
                    FOUND_IN_RELEASE_PARAMS=""
                    
                    for loc in found_in_release_filter:
                        for tmp in loc.split():
                            tmp=re.sub('[^A-Za-z0-9.]+', '', tmp)
                            if not(tmp == ""):
                                if tmp == loc.split()[-1]:
                                    FOUND_IN_RELEASE_PARAMS+="{\"term\" : { \"foundinRelease\" :\""+tmp.lower()+"\" } }"
                                else:
                                    FOUND_IN_RELEASE_PARAMS+="{\"term\" : { \"foundinRelease\" :\""+tmp.lower()+"\"} },"

                if(len(fixed_in_release_filter)>0):
                    FIXED_IN_RELEASE_PARAMS = ""
                    
                    for loc in fixed_in_release_filter:
                        for tmp in loc.split():
                            tmp=re.sub('[^A-Za-z0-9.]+', '', tmp)
                            if not(tmp == ""):
                                if tmp == loc.split()[-1]:
                                    FIXED_IN_RELEASE_PARAMS+="{\"term\" : { \"fixedinRelease\" :\""+tmp.lower()+"\" } }"
                                else:
                                    FIXED_IN_RELEASE_PARAMS+="{\"term\" : { \"fixedinRelease\" :\""+tmp.lower()+"\"} },"

                if(len(severity_filter)>0):
                    SEVERITY_PARAMS = ""
                   
                    for loc in severity_filter:
                        for tmp in loc.split():
                            tmp=re.sub('[^A-Za-z0-9]+', '', tmp)
                            if not(tmp == ""):
                                if tmp == loc.split()[-1]:
                                    SEVERITY_PARAMS+="{\"term\" : { \"severity\" :\""+tmp.lower()+"\" } }"
                                else:
                                    SEVERITY_PARAMS+="{\"term\" : { \"severity\" :\""+tmp.lower()+"\"} },"

             

                if(len(priority_filter)>0):
                    PRIORITY_PARAMS = ""
                   
                    for loc in priority_filter:
                        for tmp in loc.split():
                            tmp=re.sub('[^A-Za-z0-9]+', '', tmp)
                            if not(tmp == ""):
                                if tmp == loc.split()[-1]:
                                    PRIORITY_PARAMS+="{\"term\" : { \"priority\" :\""+tmp.lower()+"\" } }"
                                else:
                                    PRIORITY_PARAMS+="{\"term\" : { \"priority\" :\""+tmp.lower()+"\"} },"


                if(len(found_on_platform_filter)>0):
                    FOUND_ON_PLATFORM_PARAMS=""
                    
                    for loc in found_on_platform_filter:
                        for tmp in loc.split():
                            tmp=re.sub('[^A-Za-z0-9]+', '', tmp)
                            if not(tmp == ""):
                                if tmp == loc.split()[-1]:
                                    FOUND_ON_PLATFORM_PARAMS+="{\"term\" : { \"foundOnPlatform\" :\""+tmp.lower()+"\" } }"
                                else:
                                    FOUND_ON_PLATFORM_PARAMS+="{\"term\" : { \"foundOnPlatform\" :\""+tmp.lower()+"\"} },"

                if(len(date_filter)>0):
                    
                    for loc in date_filter:
                        
                        if not ("null" == str(loc)):
                            DATE_FILTER_PARAMS+="{\"range\" : { \"dateClosed\" :{ \"lte\": \""+loc.lower()+"\"}} }"
                        # for tmp in loc.split('-'):
                        #     tmp=re.sub('[^A-Za-z0-9]+', '', tmp)
                        #     if not(tmp == ""):
                        #         if tmp == loc.split('-')[-1]:
                        #             DATE_FILTER_PARAMS+="{\"term\" : { \"dateClosed\" :\""+tmp.lower()+"\" } }"
                        #         else:
                        #             DATE_FILTER_PARAMS+="{\"term\" : { \"dateClosed\" :\""+tmp.lower()+"\"} },"

                
            

            if (len(product_filter)>0):
                PARAMS+=PRODUCT_PARAMS+","
                
            if (len(group_filter)>0):
                PARAMS+=GROUP_PARAMS+","
                
            if (len(found_in_release_filter)>0):
                PARAMS+=FOUND_IN_RELEASE_PARAMS+","
                
            if (len(fixed_in_release_filter)>0):
                PARAMS+=FIXED_IN_RELEASE_PARAMS+","
                
            if (len(severity_filter)>0):
                PARAMS+=SEVERITY_PARAMS+","
                
            if (len(priority_filter)>0):
                PARAMS+=PRIORITY_PARAMS+","
                
            if (len(found_on_platform_filter)>0):
                PARAMS+=FOUND_ON_PLATFORM_PARAMS+","
                
            if ((len(date_filter)>0) and  not("null" == str(date_filter[0]))):
                PARAMS+=DATE_FILTER_PARAMS+","
                

            if((len(product_filter)>0) or (len(group_filter)>0)or (len(found_in_release_filter)>0)or (len(fixed_in_release_filter)>0)or (len(severity_filter)>0)or (len(priority_filter)>0)or (len(found_on_platform_filter)>0)or (len(date_filter)>0)):
                PARAMS = PARAMS[:-1]
                PARAMS+="]}}}}}"
            print("Devtrack Params : ",json.loads(PARAMS))
            try:

                es = Elasticsearch(config.ELK_URI, http_auth=(config.ELK_USERNAME,config.ELK_PASSWORD))
                data = es.search(index="devtrack", body=json.loads(PARAMS))
                devtrackmaxScore = data['hits']['max_score']
                devtrackList = data['hits']['hits']
                devTrack = []
                filterList={}
                filterKeys=devtrackList[0]["_source"].keys()
                for key in filterKeys:
                    filterList[key]=[]
                
                for doc in devtrackList:
                    for key in filterKeys:
                        if not (key == 'upvotedUsers' or key == 'probability' or key =='index' or key =='id' or key == 'timestamp'):
                            filterList[key].append(doc["_source"][key])
                    
                for key in filterKeys:
                        tempSet=list(set(filterList[key]))
                        filterList[key]=[]
                        for temp in tempSet:
                            if not (temp == ""):
                                filterList[key].append({"name":temp})

                for doc in devtrackList:
                    data = doc["_source"]
                    # print('DATA',data)
                    data["probability"]= round((doc["_score"]/devtrackmaxScore)*100)
                    devTrack.append(data)

                devTrackResponse={
                    "devtrack":devTrack,
                    "devtrackFilters":filterList
                }
                return devTrackResponse
            except Exception as e:
                devTrackResponse={}
                logging.error('...', exc_info=True)
                print('exception is ',e)
                return devTrackResponse
                
        def releaseNotes(search_param):

            print("Release Notes  Params : ", search_param)
            es = Elasticsearch(config.ELK_URI, http_auth=(config.ELK_USERNAME,config.ELK_PASSWORD))
            data = es.search(index="release_notes", body={"from" : 0, "size" : 50,"query": {"query_string": {"query": search_param ,"fields": ["issueId", "severity","description","workaround","file_name"]}}})
            releaseNotesmaxScore = data['hits']['max_score']
            releaseNotesList = data['hits']['hits']
           
            releaseNotes = []
            for doc in releaseNotesList:
                data = doc["_source"]
                data['key']=doc['_id'] 
                data["probability"]= round((doc["_score"]/releaseNotesmaxScore)*100)
                releaseNotes.append(data)
            return releaseNotes

        def fsb(search_param):

            print("FSB  Params : ", search_param)
            es = Elasticsearch(config.ELK_URI, http_auth=(config.ELK_USERNAME,config.ELK_PASSWORD))
            data = es.search(index="fsb", body={"from" : 0, "size" : 50,"query": {"query_string": {"query": search_param,"fields": ["issueId", "title","description","symptoms","rootCause", "file_name","FSBNumber","dateCreated","dateRevised"]}}})
            fsbmaxScore = data['hits']['max_score']
            fsbList = data['hits']['hits']
            fsb = []

            for doc in fsbList:
                data = doc["_source"]
                data['key']=doc['_id']
                data["probability"]= round((doc["_score"]/fsbmaxScore)*100)
                fsb.append(data)
            return fsb


        try:
            args = self.reqparse.parse_args()
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

            search_param = "*"+args['search_param']+"*"
            product_filter = args.get('product_filter')
            group_filter = args.get('group_filter')
            found_in_release_filter = args.get('found_in_release_filter')
            fixed_in_release_filter = args.get('fixed_in_release_filter')
            severity_filter = args.get('severity_filter')
            priority_filter = args.get('priority_filter')
            found_on_platform_filter = args.get('found_on_platform_filter')
            date_filter = args.get('date_filter')
            check_title = args.get('check_title')
            search_param=re.sub('[^A-Za-z0-9*. ]+', '', search_param)
            devTrack = devtrack(search_param,product_filter,group_filter,found_in_release_filter,fixed_in_release_filter,severity_filter,priority_filter,found_on_platform_filter,date_filter,check_title)
            releaseNotes = releaseNotes(search_param)
            fsb = fsb(search_param)
            response= {
                    "devTrack": [],
                    "releaseNotes": [],
                    "fsb": []
                }

            # For Internal Show All records ,For External Show Limited n conditions
            # keep only matching issue id in releasenotes & devtrack or service account field in devtrack is nonempty
            internal = True if args['internal'] =='true' else False
            print("internal: {0}".format(internal))

            if internal:
                response['devTrack'] = devTrack
                response['releaseNotes'] = releaseNotes
                response['fsb'] = fsb
            else:
                devTrack1={}

                # service account field in devtrack is nonempty
                devTrack1['devtrack'] = [a for a in devTrack.get('devtrack') if not a.get('serviceAccount').isspace()]
                devTrack1['devtrackFilters'] = devTrack.get('devtrackFilters')

                # keep only matching issue id in releasenotes & devtrack
                issueids_devTrack = [a.get('issueId') for a in devTrack.get('devtrack')]

                issueids_releaseNotes = [a.get('issueId').strip() for a in releaseNotes]
                common_ids = list(set(issueids_devTrack).intersection(issueids_releaseNotes))
                

                common_devTrack2= {}
                common_devTrack2['devtrack'] = [a for a in devTrack.get('devtrack') if a.get('issueId') in common_ids]
                # common_releaseNotes = [a for a in releaseNotes if a.get('issueId') in common_ids]

                # Merge devTracks one with serviceAccount & common issueid with releaseNotes

                devTrack1['devtrack'].extend(common_devTrack2.get('devtrack'))
                response['devTrack'] = devTrack1
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
            response = requests.put(config.ELK_URI+"devtrack/_doc/"+doc["issueId"],json=doc,auth=HTTPBasicAuth(config.ELK_USERNAME,config.ELK_PASSWORD),headers={"content-type":"application/json"})
            return jsonify(msg=response.json(),http_status_code=200)
        except Exception as e:
            print(e)
            return jsonify(msg="Error in Fetching Data,Please try again", http_status_code=400)

    
    def options(self):
         pass
