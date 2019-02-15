from flask import jsonify
from flask_restful import Resource
from flask_restful import reqparse
from app import Configuration
from app.auth.authorization import requires_auth
from auth0.v3.authentication import GetToken
import requests
import json


class ResetPassword(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('new_password', type=str, required=False, help='not Provided', location='json')
        self.reqparse.add_argument('user_id', type=str, required=False, help='not Provided', location='json')
        super(ResetPassword, self).__init__()

    @requires_auth
    def post(self):
        import pdb
        pdb.set_trace()
        args = self.reqparse.parse_args()
        non_interactive_client_id = Configuration.AUTH0_CLIENT_ID
        non_interactive_client_secret = Configuration.AUTH0_CLIENT_SECRET_KEY
        get_token = GetToken(Configuration.AUTH0_DOMAIN)
        token = get_token.client_credentials(non_interactive_client_id,
                                             non_interactive_client_secret,
                                             'https://{}/api/v2/'.format(Configuration.AUTH0_DOMAIN))

        mgmt_api_token = token['access_token']
        headers = {
            'Authorization': 'Bearer {0}'.format(mgmt_api_token),
            'content-type': 'application/json',
        }

        data = {"password": args.get('new_password'), "connection": "db-users"}
        data = json.dumps(data)
        routes = 'users' + '/' + args.get('user_id')
        ext_url = Configuration.AUTH0_MGMT_API + routes
        response = requests.patch(ext_url, headers=headers, data=data)

        if response.json().get('message'):
            #Message is return if their is error like password week,User does not exists
            if response.json().get('message') == "The connection does not exist.":
                return jsonify(msg="You logged in through social account ,We can't change your password", http_status_code=400)

            return jsonify(msg=response.json().get('message'), http_status_code=400)
        else:
            return jsonify(msg="Password changed Sucessfully", http_status_code=200)

    def options(self):
        pass
