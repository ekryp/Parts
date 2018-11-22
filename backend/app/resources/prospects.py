import requests
from flask_restful import Resource
from flask_restful import reqparse
import json
import os
import sys
import requests
from flask import jsonify
import glob

from app import Configuration
from app.auth.authorization import requires_auth
from app.models.basemodel import get_session
from app.models.ekryp_user import User, UserSettings
import time, calendar
from sqlalchemy import create_engine
import pandas as pd
import traceback
from datetime import datetime, timedelta
from flask import _app_ctx_stack, session, request
import json
import time
import urllib

from app.utils.utils import get_ekryp_partner_id_from_token

from app.cache import cache, has_cache_restriction, cache_key


def get_dag_status(prospects_id):
    ekryp_partner_id = prospects_id
    engine = create_engine(Configuration.AIRFLOW_DB_URL)
    query = "SELECT execution_date FROM dag_run where run_id like '{0}_%%' and dag_id = 'MLPipeline' " \
            "order by execution_date desc LIMIT 1;".format(str(ekryp_partner_id))

    result = engine.execute(query).fetchone()
    if result:
        d={}
        execution_date = result[0]
        execution_date = execution_date.strftime("%Y-%m-%d %H:%M:%S")
        #select task_id dynamically for dag_id MLPipeline
        query ="SELECT task_id FROM ekryp_challenge.task_instance where dag_id='MLPipeline' and execution_date='{0}'".format(execution_date)
        result = engine.execute(query)
        result = result.fetchall()
        for each_task in ['featureGeneration','modelGeneration']:
            task = each_task
            # to get status of DAG_ID
            URL = 'http://{0}:{1}/admin/rest_api/api?api=task_state&dag_id=MLPipeline&task_id={2}&execution_date={3}'.format(
            Configuration.AIRFLOW_HOST, Configuration.AIRFLOW_PORT, task,execution_date
            )
            response = requests.get(URL)
            status = response.json().get('output').get('stdout')
            d[task] = status
            if not 'featureGeneration' in d:
                d['featureGeneration'] = ""

            if not 'modelGeneration' in d:
                d['modelGeneration'] = ""

    else:
        d = {}
        d['featureGeneration'] = ""
        d['modelGeneration'] = ""

    return d




class ProspectsInfo(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('from_date', required = False, location='args')

    def get(self):
        args = self.reqparse.parse_args()
        auth = request.headers.get("Authorization", None)
        date_format = "%Y-%m-%d"


        try:
            # Consider the latest version of prediction result available


            queryStatus = "SELECT * FROM prospects_status as a1 left join prospect_details as a2 on  a1.prospects_id=a2.prospects_id order by a1.prospects_id,a1.prospects_step,a1.updated_date"
            ml_engine = create_engine(Configuration.PROSPECT_DB_URL)
            prospects_status_df = pd.read_sql(queryStatus, ml_engine)

            querySteps = "SELECT * FROM prospect_steps"
            ml_engine = create_engine(Configuration.PROSPECT_DB_URL)
            prospect_steps_df = pd.read_sql(querySteps, ml_engine)

            prospects_details_df = pd.merge(prospects_status_df, prospect_steps_df, left_on='prospects_step', right_on='step_id',how='inner', suffixes=('_left', '_right'))

            prospects_details_df['updated_date'] = prospects_details_df['updated_date'].apply(
                lambda date: date.strftime(date_format))


            prospects_details_df = prospects_details_df.T.drop_duplicates().T

            final = []
            d = {}
            for key, value in prospects_details_df.iterrows():

                tempstep = {
                    'prospects_step': value['prospects_step'],
                    'updated_date': value['updated_date'],
                    'step_name': value['step_name'],
                }

                try:

                    d[value['prospects_id']]['steps'].append(tempstep)
                    d[value['prospects_id']]['updated_date'] = value['updated_date']
                    d[value['prospects_id']]['step_name'] = value['step_name']
                    d[value['prospects_id']]['prospects_step'] = value['prospects_step']



                except KeyError:
                    temp = {
                        'prospects_id': value['prospects_id'],
                        'prospects_email': value['prospects_email'],
                        'updated_date': value['updated_date'],
                        'step_name': value['step_name'],
                        'steps':[],
                        'prospects_step':value['prospects_step'],
                        'ML_PIPELINE': get_dag_status(value['prospects_id'])

                    }
                    d[value['prospects_id']] = temp
                    d[value['prospects_id']]['steps'].append(tempstep)


            return d

        except Exception as e:
            print(e)
            print(traceback.print_exc())
            print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

    def options(self):
        pass



class SetProspectDone(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('prospects_id', required=True, location='json')
        super(SetProspectDone, self).__init__()

    def post(self):

        args = self.reqparse.parse_args()
        try:
            querySteps = "SELECT * FROM prospect_steps where step_name ='DONE'"
            ml_engine = create_engine(Configuration.PROSPECT_DB_URL)
            prospect_steps_df = pd.read_sql(querySteps, ml_engine)
            print(prospect_steps_df)
            for key, value in prospect_steps_df.iterrows():
                step_id = value['step_id']

            querySteps = "Insert into prospects_status values("+ str(args['prospects_id']) +","+ str(step_id) +",'"+ str((datetime.now()).strftime("%Y-%m-%d")) +"')"
            print(querySteps)
            ml_engine = create_engine(Configuration.PROSPECT_DB_URL)
            ml_engine.execute(querySteps)
            return {"message": "Updated status", "status": "success"}, 200
        except Exception as e:
            print(e)
            print(traceback.print_exc())
            print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            return {"message": "Error while action", "status": "error"}, 422

    def options(self):
        pass

class TriggerDag(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('prospects_id', required=True, location='args')
        super(TriggerDag, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        prospects_id = args['prospects_id']

        def read_conf_file(prospects_id):
            f = {"customerName":str(prospects_id)}
            conf = json.dumps(f)
            conf= urllib.parse.quote(conf)
            run_id = str(prospects_id) +'_'+ time.strftime('%Y-%m-%d %H:%M:%S')
            URL = 'http://{0}:{1}/admin/rest_api/api?api=trigger_dag&dag_id=MLPipeline&run_id={2}&conf={3}'.format(
            Configuration.AIRFLOW_HOST, Configuration.AIRFLOW_PORT,run_id ,conf
            )
            response = requests.get(URL)
            # log = response.json()
            # with open('json_response.txt', 'w') as outfile:
            #     json.dump(response.json(), outfile)
            if response.status_code == 200:
                return True
            else:
                return False

        is_triggered = read_conf_file(prospects_id)
        if is_triggered:
            return jsonify(msg="DAG Triggered", http_status_code=200)
        else:
            return jsonify(msg="DAG NOT Triggered", http_status_code=400)
    def options(self):
        pass

    def options(self):
        pass



class ExperimentDetails(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('prospects_id', required=True, location='args')
        super(ExperimentDetails, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        prospects_id = args['prospects_id']
        BASE_DIR = Configuration.BASE_DIR
        PROSPECT_DIR = os.path.join(BASE_DIR,str(prospects_id))
        EXPERIMENT_DIR = os.path.join(PROSPECT_DIR,'experiments')
        result = {}
        list_of_experiments = os.listdir(EXPERIMENT_DIR)
        result['experiments'] = result.fromkeys(list_of_experiments,{})
        for exp in list_of_experiments:
            MODEL_DIR = os.path.join(EXPERIMENT_DIR,exp)
            MODEL_DIR = os.path.join(MODEL_DIR,'Model')
            list_of_models = os.listdir(MODEL_DIR)
            result['experiments'][exp] = result.fromkeys(list_of_models, {})

            for model in list_of_models:
                RESULTS_DIR = os.path.join(MODEL_DIR, model)
                RESULTS_DIR = os.path.join(RESULTS_DIR, 'results')
                metric_file = glob.glob('{0}/*.csv'.format(RESULTS_DIR))
                if metric_file:
                    df = pd.read_csv(metric_file[0])
                    for index,row in df.iterrows():
                        if(row['metric']) == 'weightedPrecision':
                            precision = row['value']
                        if(row['metric']) == 'weightedRecall':
                            recall = row['value']
                        if(row['metric']) == 'accuracy':
                            accuracy = row['value']
                    result['experiments'][exp][model] = {'metrics':{"accuracy":accuracy,"precision":precision,"recall":recall}}



        return result

    def options(self):
        pass
