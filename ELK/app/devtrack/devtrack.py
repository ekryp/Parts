from flask import jsonify
from flask import request
import requests
import re
import config
from app.common import escapeESArg
from requests.auth import HTTPBasicAuth
from flask_restful import Resource
from flask_restful import reqparse
import csv, json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from elasticsearch import Elasticsearch
import logging
from operator import itemgetter


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
        self.reqparse.add_argument('service_account_filter', required=False, location='args', action='append')
        self.reqparse.add_argument('check_title',required=False,help='check_title',location='args')
        self.reqparse.add_argument('internal', required=False, location='args')
        super(DevTrackData, self).__init__()

    def get(self):

        def devtrack(search_param,product_filter,group_filter,found_in_release_filter,fixed_in_release_filter,severity_filter,priority_filter,found_on_platform_filter,date_filter,checkTitle,service_account_filter):
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
            if not(isinstance(service_account_filter,list)):
                service_account_filter=[]

            DATE_FILTER_PARAMS=""
            
            URL=config.ELK_URI+"devtrack/_doc/_search"
            headers = {'Content-type': 'application/json'}
            if((len(product_filter)==0) and (len(group_filter)==0)and (len(found_in_release_filter)==0)and (len(fixed_in_release_filter)==0)and (len(severity_filter)==0)and (len(priority_filter)==0)and (len(found_on_platform_filter)==0)and (len(date_filter)==0)and (len(service_account_filter)==0)):
                print(check_title)
                if(check_title == "true"):
                    PARAMS = "{\"from\" : 0, \"size\" : 10000,\"query\": {\"query_string\": {\"query\": \""+search_param+"\",\"fields\": [\"title\"]}}}"
                else:
                    PARAMS = "{\"from\" : 0, \"size\" : 10000,\"query\": {\"query_string\": {\"query\": \""+search_param+"\",\"fields\": [ \"severity\",\"description\",\"foundinRelease\",\"issueId\"]}}}"

            else:
                if(check_title == "true"):
                    PARAMS="{\"from\" : 0, \"size\" : 10000,\"query\": {\"bool\": {\"must\": {\"query_string\": {\"query\": \""+search_param+"\",\"fields\": [\"title\"]}},\"filter\": {\"bool\" : {\"must\" : ["
                else:
                    PARAMS="{\"from\" : 0, \"size\" : 10000,\"query\": {\"bool\": {\"must\": {\"query_string\": {\"query\": \""+search_param+"\"}},\"filter\": {\"bool\" : {\"must\" : ["
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


                if(len(service_account_filter)>0):
                    SERVICE_ACCOUNT_PARAMS=""
                    for loc in service_account_filter:
                        for tmp in loc.split():
                            tmp=re.sub('[^A-Za-z0-9]+', '', tmp)
                            if not(tmp == ""):
                                if tmp == loc.split()[-1]:
                                    SERVICE_ACCOUNT_PARAMS+="{\"term\" : { \"serviceAccount\" :\""+tmp.lower()+"\" } }"
                                else:
                                    SERVICE_ACCOUNT_PARAMS+="{\"term\" : { \"serviceAccount\" :\""+tmp.lower()+"\"} },"


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

            if (len(service_account_filter)>0):
                PARAMS+=SERVICE_ACCOUNT_PARAMS+","
                
            if (len(found_on_platform_filter)>0):
                PARAMS+=FOUND_ON_PLATFORM_PARAMS+","
                
            if ((len(date_filter)>0) and  not("null" == str(date_filter[0]))):
                PARAMS+=DATE_FILTER_PARAMS+","
                

            if((len(product_filter)>0) or (len(group_filter)>0)or (len(found_in_release_filter)>0)or (len(fixed_in_release_filter)>0)or (len(severity_filter)>0)or (len(priority_filter)>0)or (len(found_on_platform_filter)>0)or (len(date_filter)>0)or (len(service_account_filter)>0)):
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
                if(len(devtrackList)>0):
                    filterKeys=devtrackList[0]["_source"].keys()
                    for key in filterKeys:
                        filterList[key]=[]
                    
                    for doc in devtrackList:
                        for key in filterKeys:
                            
                            # print('value ----->',doc["_source"][key])
                            if  (key == 'product' or key == 'group' or key =='severity' or key =='priority' or key == 'foundinRelease' or key == 'fixedinRelease' or key == 'dateClosed' or key == 'serviceAccount'):
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
            data = es.search(index="release_notes", body={"from" : 0, "size" : 10000,"query": {"query_string": {"query": search_param ,"fields": ["issueId", "severity","description","workaround","file_name"]}}})
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
            data = es.search(index="fsb", body={"from" : 0, "size" : 10000,"query": {"query_string": {"query": search_param,"fields": ["issueId", "title","description","symptoms","rootCause", "file_name","FSBNumber","dateCreated","dateRevised"]}}})
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

            
            product_filter = args.get('product_filter')
            group_filter = args.get('group_filter')
            found_in_release_filter = args.get('found_in_release_filter')
            fixed_in_release_filter = args.get('fixed_in_release_filter')
            severity_filter = args.get('severity_filter')
            priority_filter = args.get('priority_filter')
            found_on_platform_filter = args.get('found_on_platform_filter')
            date_filter = args.get('date_filter')
            check_title = args.get('check_title')
            service_account_filter=args.get('service_account_filter')
            search_param = escapeESArg(args['search_param'])
            splited_search_param = search_param.split(' ')
            updated_search_param = splited_search_param[0]
            for tmp in splited_search_param[1:]:
                updated_search_param += " AND "+tmp

            search_param = updated_search_param
            devTrack = devtrack(search_param,product_filter,group_filter,found_in_release_filter,fixed_in_release_filter,severity_filter,priority_filter,found_on_platform_filter,date_filter,check_title,service_account_filter)
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
                devTrack1['devtrack'] = [a for a in devTrack.get('devtrack') if not (a.get('serviceAccount').isspace() or a.get('serviceAccount') =='' ) ]
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



class DevTrackPhrasePrefix(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('search_param', required=False, help='search_param', location='args')
        self.reqparse.add_argument('predict_value', required=False, help='predict_value', location='args')
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
        self.reqparse.add_argument('service_account_filter', required=False, location='args', action='append')
        self.reqparse.add_argument('check_title',required=False,help='check_title',location='args')
        self.reqparse.add_argument('internal', required=False, location='args')
        self.reqparse.add_argument('phrase_query', required=False, location='args', action='append')

        
        super(DevTrackPhrasePrefix, self).__init__()

    def get(self):

        def devtrack(search_param,product_filter,group_filter,found_in_release_filter,fixed_in_release_filter,severity_filter,priority_filter,found_on_platform_filter,date_filter,checkTitle,service_account_filter,phrase_query,final_list):
            try:
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
                if not(isinstance(service_account_filter,list)):
                    service_account_filter=[]
                if not(isinstance(phrase_query,list)):
                    phrase_query=[]
                search_param_list = search_param.split(' ')
                if(len(phrase_query)>0):
                    for phrase in phrase_query:
                        search_param_list.append(phrase)
                search_param_list = list( dict.fromkeys(search_param_list)) 
                DATE_FILTER_PARAMS=""
                PARAMS=""
                URL=config.ELK_URI+"devtrack/_doc/_search"
                headers = {'Content-type': 'application/json'}
                if((len(product_filter)==0) and (len(group_filter)==0)and (len(found_in_release_filter)==0)and (len(fixed_in_release_filter)==0)and (len(severity_filter)==0)and (len(priority_filter)==0)and (len(found_on_platform_filter)==0)and (len(date_filter)==0)and (len(service_account_filter)==0)):
                    print(check_title)
                    if(check_title == "true"):
                        PARAMS="{\"from\" : 0, \"size\" : 10000,\"query\": {\"bool\": {\"must\": ["
                        
                        if(len(search_param_list)>0):
                            for tmp in search_param_list:
                                
                                #tmp=re.sub('[^A-Za-z0-9.- ]+ ', '', tmp)
                                if not(tmp == ""):
                                    if tmp == search_param_list[-1]:
                                        PARAMS+="{\"multi_match\": {\"query\": \""+tmp+"\",\"fields\": [\"title\"],\"type\" : \"phrase_prefix\"}},"
                                    else:
                                        PARAMS+="{\"multi_match\": {\"query\": \""+tmp+"\",\"fields\": [\"title\"],\"type\" : \"phrase_prefix\"}},"

                        if(len(final_list)>0):
                            
                            for tmp_list in final_list:
                                PARAMS+=" {\"bool\": {\"should\": ["
                                for tmp in tmp_list:
                                    #tmp=re.sub('[^A-Za-z0-9.- ]+', '', tmp)
                                    if not(tmp == ""):
                                        if tmp == tmp_list[-1]:
                                            PARAMS+="{\"multi_match\": {\"query\": \""+tmp+"\",\"fields\": [\"title\"],\"type\" : \"phrase_prefix\"}}"
                                        else:
                                            PARAMS+="{\"multi_match\": {\"query\": \""+tmp+"\",\"fields\": [\"title\"],\"type\" : \"phrase_prefix\"}},"
                                PARAMS+="]}},"
                        
                        PARAMS=PARAMS[:-1]
                        PARAMS+="]}}}"

                    
                    else:
                        PARAMS="{\"from\" : 0, \"size\" : 10000,\"query\": {\"bool\": {\"must\": ["
                        
                        if(len(search_param_list)>0):
                            for tmp in search_param_list:
                                
                                #tmp=re.sub('[^A-Za-z0-9.- ]+', '', tmp)
                                if not(tmp == ""):
                                    if tmp == search_param_list[-1]:
                                        PARAMS+="{\"multi_match\": {\"query\": \""+tmp+"\",\"type\" : \"phrase_prefix\"}},"
                                    else:
                                        PARAMS+="{\"multi_match\": {\"query\": \""+tmp+"\",\"type\" : \"phrase_prefix\"}},"

                        if(len(final_list)>0):
                            
                            for tmp_list in final_list:
                                PARAMS+=" {\"bool\": {\"should\": ["
                                for tmp in tmp_list:
                                    #tmp=re.sub('[^A-Za-z0-9.- ]+', '', tmp)
                                    if not(tmp == ""):
                                        if tmp == tmp_list[-1]:
                                            PARAMS+="{\"multi_match\": {\"query\": \""+tmp+"\",\"type\" : \"phrase_prefix\"}}"
                                        else:
                                            PARAMS+="{\"multi_match\": {\"query\": \""+tmp+"\",\"type\" : \"phrase_prefix\"}},"
                                PARAMS+="]}},"
                        
                        PARAMS=PARAMS[:-1]
                        PARAMS+="]}}}"

                else:
                    # if(check_title == "true"):
                    #     PARAMS="{\"from\" : 0, \"size\" : 50,\"query\": {\"bool\": {\"must\": {\"multi_match\": {\"query\": \""+phrase_query[0]+"\",\"fields\": [\"title\"],\"type\" : \"phrase_prefix\"}},\"filter\": {\"bool\" : {\"must\" : ["
                    # else:
                    #     PARAMS="{\"from\" : 0, \"size\" : 50,\"query\": {\"bool\": {\"must\": {\"multi_match\": {\"query\": \""+phrase_query[0]+"\",\"type\" : \"phrase_prefix\"}},\"filter\": {\"bool\" : {\"must\" : ["



                    if(check_title == "true"):
                        PARAMS="{\"from\" : 0, \"size\" : 10000,\"query\": {\"bool\": {\"must\": ["
                        
                        if(len(search_param_list)>0):
                            for tmp in search_param_list:
                                
                                #tmp=re.sub('[^A-Za-z0-9.-]+', '', tmp)
                                if not(tmp == ""):
                                    if tmp == search_param_list[-1]:
                                        PARAMS+="{\"multi_match\": {\"query\": \""+tmp+"\",\"fields\": [\"title\"],\"type\" : \"phrase_prefix\"}},"
                                    else:
                                        PARAMS+="{\"multi_match\": {\"query\": \""+tmp+"\",\"fields\": [\"title\"],\"type\" : \"phrase_prefix\"}},"

                        if(len(final_list)>0):
                            
                            for tmp_list in final_list:
                                PARAMS+=" {\"bool\": {\"should\": ["
                                for tmp in tmp_list:
                                    #tmp=re.sub('[^A-Za-z0-9.-]+', '', tmp)
                                    if not(tmp == ""):
                                        if tmp == tmp_list[-1]:
                                            PARAMS+="{\"multi_match\": {\"query\": \""+tmp+"\",\"fields\": [\"title\"],\"type\" : \"phrase_prefix\"}}"
                                        else:
                                            PARAMS+="{\"multi_match\": {\"query\": \""+tmp+"\",\"fields\": [\"title\"],\"type\" : \"phrase_prefix\"}},"
                                PARAMS+="]}},"
                        PARAMS=PARAMS[:-1]
                        PARAMS+="],\"filter\": {\"bool\" : {\"must\" : ["
                        

                    
                    else:
                        PARAMS="{\"from\" : 0, \"size\" : 10000,\"query\": {\"bool\": {\"must\": ["
                        
                        if(len(search_param_list)>0):
                            for tmp in search_param_list:
                                
                                #tmp=re.sub('[^A-Za-z0-9.-]+', '', tmp)
                                if not(tmp == ""):
                                    if tmp == search_param_list[-1]:
                                        PARAMS+="{\"multi_match\": {\"query\": \""+tmp+"\",\"type\" : \"phrase_prefix\"}},"
                                    else:
                                        PARAMS+="{\"multi_match\": {\"query\": \""+tmp+"\",\"type\" : \"phrase_prefix\"}},"

                        if(len(final_list)>0):
                            
                            for tmp_list in final_list:
                                PARAMS+=" {\"bool\": {\"should\": ["
                                for tmp in tmp_list:
                                    #tmp=re.sub('[^A-Za-z0-9.-]+', '', tmp)
                                    if not(tmp == ""):
                                        if tmp == tmp_list[-1]:
                                            PARAMS+="{\"multi_match\": {\"query\": \""+tmp+"\",\"type\" : \"phrase_prefix\"}}"
                                        else:
                                            PARAMS+="{\"multi_match\": {\"query\": \""+tmp+"\",\"type\" : \"phrase_prefix\"}},"
                                PARAMS+="]}},"
                        PARAMS=PARAMS[:-1]
                        PARAMS+="],\"filter\": {\"bool\" : {\"must\" : ["





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


                    if(len(service_account_filter)>0):
                        SERVICE_ACCOUNT_PARAMS=""
                        for loc in service_account_filter:
                            for tmp in loc.split():
                                tmp=re.sub('[^A-Za-z0-9]+', '', tmp)
                                if not(tmp == ""):
                                    if tmp == loc.split()[-1]:
                                        SERVICE_ACCOUNT_PARAMS+="{\"term\" : { \"serviceAccount\" :\""+tmp.lower()+"\" } }"
                                    else:
                                        SERVICE_ACCOUNT_PARAMS+="{\"term\" : { \"serviceAccount\" :\""+tmp.lower()+"\"} },"


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

                    if (len(service_account_filter)>0):
                        PARAMS+=SERVICE_ACCOUNT_PARAMS+","
                        
                    if (len(found_on_platform_filter)>0):
                        PARAMS+=FOUND_ON_PLATFORM_PARAMS+","
                        
                    if ((len(date_filter)>0) and  not("null" == str(date_filter[0]))):
                        PARAMS+=DATE_FILTER_PARAMS+","
                        

                    
                    PARAMS = PARAMS[:-1]
                # PARAMS+= "]{\"should\" : ["
                
                # if(len(search_param_list)>0):
                #         SEARCH_PARAMS=""
                        
                #         for tmp in search_param_list:
                           
                        
                #             tmp=re.sub('[^A-Za-z0-9.-]+', '', tmp)
                #             if not(tmp == ""):
                #                 if tmp == search_param_list[-1]:
                #                     SEARCH_PARAMS+="{\"term\" : { \"description\" :\""+tmp.lower()+"\" } },"
                #                 else:
                #                     SEARCH_PARAMS+="{\"term\" : { \"description\" :\""+tmp.lower()+"\"} },"


                #         for tmp1 in search_param_list:
                            
                #             tmp1=re.sub('[^A-Za-z0-9.-]+', '', tmp1)
                #             if not(tmp1 == ""):
                #                 if tmp1 == search_param_list[-1]:
                #                     SEARCH_PARAMS+="{\"term\" : { \"title\" :\""+tmp1.lower()+"\" } }"
                #                 else:
                #                     SEARCH_PARAMS+="{\"term\" : { \"title\" :\""+tmp1.lower()+"\"} },"

                # if (len(search_param_list)>0):
                #         PARAMS+=SEARCH_PARAMS+","
                    #PARAMS = PARAMS[:-1]
                    PARAMS+="]}}}}}"
                    #PARAMS+="]}}}}"
                print("Devtrack Params : ",PARAMS)
                

                es = Elasticsearch(config.ELK_URI, http_auth=(config.ELK_USERNAME,config.ELK_PASSWORD))
                data = es.search(index="devtrack", body=json.loads(PARAMS))
                print('data needed ',data)
                devtrackmaxScore = data['hits']['max_score']
                devtrackList = data['hits']['hits']
                devTrack = []
                filterList={"product":[],"group":[],"severity":[],"priority":[],"foundinRelease":[],"fixedinRelease":[],"dateClosed":[],"serviceAccount":[]}
                if(len(devtrackList)>0):
                    filterKeys=devtrackList[0]["_source"].keys()
                    for key in filterKeys:
                        filterList[key]=[]
                    
                    for doc in devtrackList:
                        for key in filterKeys:
                            
                            # print('value ----->',doc["_source"][key])
                            if (key in doc["_source"].keys()):
                                filterList[key].append(doc["_source"][key])
                            #if  (key == 'product' or key == 'group' or key =='severity' or key =='priority' or key == 'foundinRelease' or key == 'fixedinRelease' or key == 'dateClosed' or key == 'serviceAccount'):
                            #    filterList[key].append(doc["_source"][key])
                        
                    for key in filterKeys:
                            try:
                                tempSet=list(set(filterList[key]))
                            except:
                                # Converting a nested list to a set
                                '''
                                >>> a = [1,2,3,4,[5,6,7],8,9]
                                >>> set(a)
                                Traceback (most recent call last):
                                 File "<stdin>", line 1, in <module>
                                TypeError: unhashable type: 'list'
                                We have upvotedUsers= [['user1@email.com'],['user1@email.com']]
                                which was causing trouble
                                '''
                                tempSet = list(set([item for sublist in filterList[key] for item in sublist]))

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
            



        def releaseNotes(search_param,phrase_query,final_list):
            if not(isinstance(phrase_query,list)):
                phrase_query=[]
            search_param_list = search_param.split(' ')
            if(len(phrase_query)>0):
                for phrase in phrase_query:
                    search_param_list.append(phrase)
        
            search_param_list = list( dict.fromkeys(search_param_list))
            print("Release Notes  Params : ", search_param)
            es = Elasticsearch(config.ELK_URI, http_auth=(config.ELK_USERNAME,config.ELK_PASSWORD))
            PARAMS="{\"from\" : 0, \"size\" : 10000,\"query\": {\"bool\": {\"must\": ["
                        
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


            data = es.search(index="release_notes",body=json.loads(PARAMS))
            releaseNotesmaxScore = data['hits']['max_score']
            releaseNotesList = data['hits']['hits']
           
            releaseNotes = []
            for doc in releaseNotesList:
                data = doc["_source"]
                data['key']=doc['_id'] 
                data["probability"]= round((doc["_score"]/releaseNotesmaxScore)*100)
                releaseNotes.append(data)
            return releaseNotes

        def fsb(search_param,phrase_query,final_list):
            if not(isinstance(phrase_query,list)):
                phrase_query=[]
            search_param_list = search_param.split(' ')
            if(len(phrase_query)>0):
                for phrase in phrase_query:
                    search_param_list.append(phrase)
        

            print("FSB  Params : ", search_param)
            PARAMS="{\"from\" : 0, \"size\" : 10000,\"query\": {\"bool\": {\"must\": ["
                        
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
            es = Elasticsearch(config.ELK_URI, http_auth=(config.ELK_USERNAME,config.ELK_PASSWORD))
            data = es.search(index="fsb",body=json.loads(PARAMS))
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

            
            product_filter = args.get('product_filter')
            group_filter = args.get('group_filter')
            found_in_release_filter = args.get('found_in_release_filter')
            fixed_in_release_filter = args.get('fixed_in_release_filter')
            severity_filter = args.get('severity_filter')
            priority_filter = args.get('priority_filter')
            found_on_platform_filter = args.get('found_on_platform_filter')
            date_filter = args.get('date_filter')
            check_title = args.get('check_title')
            service_account_filter=args.get('service_account_filter')
            search_param = args['search_param']
            phrase_query= args['phrase_query']
            predict_value = args['predict_value']
            search_param = escapeESArg(search_param)
            search_param=re.sub(' +', ' ', search_param)
            print('search Param',search_param)
            print('phrase_query Param',phrase_query)
            print('predict_value Param',predict_value)
            predict_value_list=predict_value.split(",")
            final_list=[]
            if (len(predict_value_list)>0):
                predict_value_list.pop(0)    
                for predict_list in predict_value_list:
                    filter_list=[]
                    for tmp in predict_list.split('|')[1:]:
                        filter_list.append(tmp)
                    final_list.append(filter_list)    
                print('filter list ',final_list)
            devTrack = devtrack(search_param,product_filter,group_filter,found_in_release_filter,fixed_in_release_filter,severity_filter,priority_filter,found_on_platform_filter,date_filter,check_title,service_account_filter,phrase_query,final_list)
            releaseNotes = releaseNotes(search_param,phrase_query,final_list)
            fsb = fsb(search_param,phrase_query,final_list)
            response= {
                    "devTrack": [],
                    "releaseNotes": [],
                    "fsb": []
                    
                }

            internal = True if args['internal'] =='true' else False
            print("internal: {0}".format(internal))

            if internal:
                response['devTrack'] = devTrack
                response['releaseNotes'] = releaseNotes
                response['fsb'] = fsb
            else:
                devTrack1={}

                # service account field in devtrack is nonempty
                devTrack1['devtrack'] = [a for a in devTrack.get('devtrack') if not (a.get('serviceAccount').isspace() or a.get('serviceAccount') =='' ) ]
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
                print("Before Confidence score : {0}".format([int(a.get('probability')) for a in devTrack1.get('devtrack')]))

                try:
                    # throws error if devTrack1 is empty list
                    max_score = max([int(a.get('probability')) for a in devTrack1.get('devtrack')])

                    for record in devTrack1['devtrack']:
                        # print(max_score)
                        # print(record.get("probability"))
                        record["probability"] = round((record.get("probability") / max_score) * 100)
                        # print(record.get("probability"))

                except:
                    pass

                print("After Confidence score : {0}".format([int(a.get('probability')) for a in devTrack1.get('devtrack')]))

                # Filter by probability in descending order
                devTrack1['devtrack'] = sorted(devTrack1['devtrack'], key=itemgetter('probability'), reverse=True)

                print("Order by Confidence score : {0}".format([int(a.get('probability')) for a in devTrack1.get('devtrack')]))

                response['devTrack'] = devTrack1
                response['releaseNotes'] = releaseNotes
                response['fsb'] = fsb
            return jsonify(data=response, http_status_code=200)
           
        except Exception as e:
            print(e)
            return jsonify(msg="Error in Fetching Data,Please try again", http_status_code=500)


    
    def options(self):
         pass

