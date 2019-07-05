import requests
from flask_restful import Resource
from flask_restful import reqparse
import json

from app import Configuration
from app.auth.authorization import requires_auth
from app.models.basemodel import get_session
from app.models.ekryp_user import User, UserSettings
from app.models.ekryp_user_session import UserSession
from app.resources.constants import EkrypAPI
from app.utils.utils import Utils, logged_in_users, get_user_id_from_token, remove_token_from_dict, get_ekryp_partner_id_from_token, get_df_from_sql_query

import time, calendar
from datetime import datetime, timedelta
from flask import _app_ctx_stack, session, request
import json
from sqlalchemy import create_engine
from sqlalchemy import exc

from app.cache import cache, has_cache_restriction, cache_key


class EkrypCache(Resource):
    def __init__(self):
        super(EkrypCache, self).__init__()

    @requires_auth
    @cache.cached(timeout=60 * 60 * 24 * 7, key_prefix=cache_key, unless=has_cache_restriction)
    def get(self):
        import datetime
        return str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    @requires_auth
    def delete(self):
        import datetime
        cache.clear()
        return str("Cleared the cache at: {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))



def authenticate(username, password):
    session = get_session()
    user = session.query(User).filter_by(username=username).first()
    if user and user.verify_password(password):
        return user


def identity(payload):
    user_id = payload['identity']
    session = get_session()
    return session.query(User).filter_by(id=user_id).first()



class Callback(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email_id', type=str, required=True, help='not Provided', location='json')
        self.reqparse.add_argument('ekryp_partner_id', type=int, required=True, help='not Provided', location='json')
        self.reqparse.add_argument('first_name', type=str, required=False, help='not Provided', location='json')
        self.reqparse.add_argument('last_name', type=str, required=False, help='not Provided', location='json')
        self.reqparse.add_argument('phone_no', type=str, required=False, help='not Provided', location='json')
        self.reqparse.add_argument('address', type=str, required=False, help='not Provided', location='json')
        self.reqparse.add_argument('role_id', type=int, required=False, help='not Provided', location='json')
        super(Callback, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        settings = '{"geo":[],"incident_category":[],"priority":[],"country":[],"state":[],"model_group":[],"model_name":[],"firmware_name":[],"company_name":[],"service_provider_name":[],"from_dttm":"2017-07-01","to_dttm":"2017-08-18","time_bucket":{"granularity":"quarter"},"timeslot":"cq","row_limit":10,"against":"customer_asset_identifier","time":"selected","rate_by_assets":{"age_or_work":"age","compare":false,"model_name":[],"company_name":[],"timeslot":"lfy","from_dttm":"2016-01-01","to_dttm":"2016-12-31"},"model_group_name":[]}'
        dash_settings = '[{"name":"Incidents Over Time","id":"TrendOverTime","url":"trend-over-time","order":1,"display":true},{"name":"Incident Count By Asset","id":"TrendByAssets","url":"trend-by-assets","order":2,"display":true},{"name":"Asset Failure Rates","id":"RateByAssets","url":"rate-by-assets","order":3,"display":true},{"name":"Incident Type Analysis","id":"DistributionByType","url":"distribution-by-type","order":4,"display":true},{"name":"Incidents By Asset Model","id":"DistributionByModel","url":"distribution-by-model","order":5,"display":true},{"name":"Remediation By Incident Type","id":"SolutionMap","url":"solution-map","order":6,"display":true},{"name":"Remediation Solution Effectiveness","id":"SolutionEffectiveness","url":"solution-effectiveness","order":7,"display":true},{"name":"Incidents By Asset Age","id":"TrendByAge","url":"trend-by-age","order":8,"display":true},{"name":"Incidents By Work Performed","id":"TrendByNotes","url":"trend-by-notes","order":9,"display":true},{"name":"Incremental Failure Rate Trend","id":"IncrementalFailureRateTrend","url":"incremental-failure-rate-trend","order":10,"display":true}]'
        display_settings = '{"GraphSettings":{"name":"Incident Display","data":[{"name":"Show Label Inside Graph","id":"ShowLabelInsideGraph","display":false,"type":"GraphSetting"},{"name":"Preventative Maintenance","id":"PreventativeMaintenance","display":true,"type":"GraphSetting"},{"name":"Cleaning Supplies","id":"CleaningSupplies","display":true,"type":"GraphSetting"},{"name":"Incident Count By Asset 80/20 Rule(%)","id":"TrendByAssets80_20Rule","value":80,"displayType":"text","type":"GraphSetting"},{"name":"Solution Effectiveness within days","id":"SolutionEffectiveness_EffectivenessMetricsInDays","value":5,"displayType":"text","type":"GraphSetting"}]},"TableSettings":{"name":"Asset Reports","data":[{"name":"Asset Id","id":"device_id","display":false,"type":"Product"},{"name":"Serial Number","id":"derived_serial_number","display":true,"type":"Product"},{"name":"Company Name","id":"company_name","display":true,"type":"Product"},{"name":"Service Provider Name","id":"service_provider_name","display":true,"type":"Product"},{"name":"Firmware Name","id":"firmware_name","display":true,"type":"Product"},{"name":"Age","id":"device_age","display":true,"type":"Product"},{"name":"Notes Processed","id":"cumulative_work_done","display":true,"type":"Product"},{"name":"Model","id":"model_name","display":true,"type":"Product"},{"name":"Installed Date","id":"installed_date","display":true,"type":"Product"},{"name":"Incident Count","id":"incident_count","display":true,"type":"Product"}]}}'
        prediction_settings = '{"DisplaySettings":{"name":"Prediction Display Settings","data":[{"name":"Allow Prediction Date Selection","id":"AllowPredictionDateSelection","display":true,"type":"DisplaySettings","value":true}]},"CalculationSettings":{"name":"Prediction Calculation Settings","data":[{"name":"Prediction Summary X days","id":"PredictionSummaryXDays","display":true,"value":10,"displayType":"text","type":"GraphSetting"},{"name":"Prediction Summary of Top X product","id":"PredictionSummaryProductFailureTopLimit","display":true,"value":20,"displayType":"text","type":"ReportSetting"},{"name":"Incident Categories for Action Taken","id":"IncidenCategories","display":true,"value":["Preventative Maintenance"],"displayType":"multi-select","type":"PredictionSetting","optionsConfigURL":"IncidentCategories"},{"name":"Highlight Incidents Open for more than X days","id":"IncidentMaxXDays","display":true,"value":20,"displayType":"text","type":"PredictionSetting"},{"name":"Model Characteristics using next X days prediction","id":"ModelCharacteristicsByNextXDays","display":true,"value":30,"displayType":"text","type":"PredictionSetting"}]}}'
        access_token_data = get_access_token()
        access_token = access_token_data['access_token']
        db_session = get_session()
        dupl = db_session.query(User).filter_by(email_id=args['email_id']).first()
        engine = create_engine(Configuration.EKRYP_USER_DB_URI)
        try:
            ekryp_partner_id = args['ekryp_partner_id']
            email_id = args['email_id']
            query = "insert into ekryp_partner (id,status,partner_name) values({0},1,'{1}')".format(ekryp_partner_id,email_id)
            engine.execute(query)
        except exc.IntegrityError as e:
            print("INFO :: ekryp_partner_id : {0} and email_id: '{1}' is already present in table ekryp_partner ".format(ekryp_partner_id,email_id))
        try:
            data_engine = create_engine(Configuration.EKRYP_DATA_DB_URI)
            cust_id = args['ekryp_partner_id']
            cust_name = args['email_id']
            query = "insert into customer (cust_id,cust_status,cust_name) values({0},1,'{1}')".format(cust_id,cust_name)
            data_engine.execute(query)
        except exc.IntegrityError as e:
            print("INFO :: cust_id : {0} and cust_name: '{1}' is already present in table customer ".format(cust_id,cust_name))
        try:
            data_engine = create_engine(Configuration.EKRYP_DATA_DB_URI)
            cust_id = args['ekryp_partner_id']
            query = "insert into failure_probability (cust_id) values({0})".format(cust_id)
            data_engine.execute(query)
        except exc.IntegrityError as e:
            print("INFO :: cust_id : {0}  is already present in table failure_probability ".format(cust_id))

        if dupl is None:
            user = User(ekryp_partner_id=args['ekryp_partner_id'], first_name=args['first_name'],
                        last_name=args['last_name'], settings=settings, dash_settings=dash_settings,
                        email_id=args['email_id'], phone_no=args['phone_no'], address=args['address'],
                        role_id=args['role_id'])
            db_session.add(user)
            db_session.commit()
            if user:
                dupl_display_settings = db_session.query(UserSettings).filter_by(ekryp_user=user.id,
                                                                                 name="display_settings").first()
                if dupl_display_settings is None:
                    disp_settings = UserSettings(ekryp_user=user.id, name="display_settings", data=display_settings)
                    db_session.add(disp_settings)
                dupl_prediction_settings = db_session.query(UserSettings).filter_by(ekryp_user=user.id,
                                                                                    name="prediction_settings").first()
                if dupl_prediction_settings is None:
                    pred_settings = UserSettings(ekryp_user=user.id, name="prediction_settings",
                                                 data=prediction_settings)
                    db_session.add(pred_settings)
                    db_session.commit()
                user_session_dupl = db_session.query(UserSession).filter_by(access_token=access_token).first()
                if user_session_dupl is None:
                    user_session = UserSession(access_token=access_token, user_id=user.id,
                                               ekryp_partner_id=user.ekryp_partner_id)
                    db_session.add(user_session)
                    db_session.commit()
                logged_in_users[access_token] = {"user_id": user.id, "ekryp_partner_id": user.ekryp_partner_id}
        else:
            print(dupl.ekryp_partner_id)
            user_session_dupl = db_session.query(UserSession).filter_by(access_token=access_token).first()
            if user_session_dupl is None:
                user_session = UserSession(access_token=access_token, user_id=dupl.id,
                                           ekryp_partner_id=dupl.ekryp_partner_id)
                db_session.add(user_session)
                db_session.commit()
            logged_in_users[access_token] = {"user_id": dupl.id, "ekryp_partner_id": dupl.ekryp_partner_id}

        return {"data": access_token_data, "identity": args['email_id'], "status": "success"}, 200

    def options(self):
        pass


def get_access_token():
    body = {
        "client_id": Configuration.AUTH0_CLIENT_ID,
        "client_secret": Configuration.AUTH0_CLIENT_SECRET_KEY,
        "audience": Configuration.AUTH0_API_AUDIENCE,
        "grant_type": EkrypAPI.grant_type.value
    }
    header = {
        "content-type": EkrypAPI.content_type.value
    }
    res = requests.post(EkrypAPI.token_get_url.value, json=body, headers=header)
    res_json = json.loads(res.text)

    return res_json


class Logout(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(Logout, self).__init__()

    @requires_auth
    def post(self):
        args = self.reqparse.parse_args()
        auth = request.headers.get("Authorization", None)
        token = remove_token_from_dict(auth)
        db_session = get_session()
        user_session_dupl = db_session.query(UserSession).filter_by(access_token=token).first()
        if user_session_dupl:
            db_session.delete(user_session_dupl)
            db_session.commit()
        return {"message": "User logged out successfully", "status": "success"}, 200

    def options(self):
        pass
