import requests
from flask_restful import Resource
from flask_restful import reqparse
import json
from flask import jsonify
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
        self.reqparse.add_argument('username', type=str, required=True, help='Please provide username or email', location='json')
        self.reqparse.add_argument('password', type=str, required=True, help='Please provide password', location='json')
        super(Callback, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        print(args.get('username'))
        url = "https://ekryp.auth0.com/oauth/token"
        payload = {"grant_type": "password",
                   "username": args.get('username'),
                   "password": args.get('password'),
                   "client_id": Configuration.AUTH0_CLIENT_ID,
                   "client_secret": Configuration.AUTH0_CLIENT_SECRET_KEY,
                   "audience": Configuration.AUTH0_API_AUDIENCE
                   }
        payload = json.dumps(payload)

        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache"
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        if response.status_code == 200:
            return jsonify(access_token= response.json().get('access_token'), http_status_code=200)
        return jsonify(msg=response.json().get('error_description'), http_status_code=response.status_code)

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
