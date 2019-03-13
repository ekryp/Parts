import urllib

import requests
from flask import request, jsonify
from flask import _app_ctx_stack
import json
from flask_restful import Resource, reqparse

from jose import jwt
from six.moves.urllib.request import urlopen
from functools import wraps

from app import Configuration

ALGORITHMS = ["RS256"]
ISSUER = 'https://ekryp.auth0.com/'


def get_token_auth_header():
    """Obtains the access token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        return ({"code": "authorization_header_missing",
                "description": "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        return ({"code": "invalid_header",
                "description":"Authorization header must start with Bearer"}, 401)
    elif len(parts) == 1:
        return ({"code": "invalid_header",
                "description": "Token not found"}, 401)
    elif len(parts) > 2:
        return ({"code": "invalid_header",
                "description": "Authorization header must be Bearer token"}, 401)

    token = parts[1]
    return token


def requires_scope(required_scope):
    """Determines if the required scope is present in the access token
    Args:
        required_scope (str): The scope required to access the resource
    """
    token = get_token_auth_header()
    unverified_claims = jwt.get_unverified_claims(token)
    token_scopes = unverified_claims["scope"].split()
    for token_scope in token_scopes:
        if token_scope == required_scope:
            return True
    return False


def requires_auth(f):
    """Determines if the access token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()

        jsonurl = urlopen("https://"+Configuration.AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read().decode('utf-8'))
        try:
            unverified_header = jwt.get_unverified_header(token)
        except jwt.JWTError:
            return ({"code": "invalid_header",
                    "description": "Invalid header. Use an RS256 signed JWT Access Token"}, 401)
        if unverified_header["alg"] == "HS256":
            return ({"code": "invalid_header",
                    "description": "Invalid header. Use an RS256 signed JWT Access Token"}, 401)
        rsa_key = ''
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }

        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=Configuration.AUTH0_API_AUDIENCE,
                    issuer=ISSUER
                )
            except jwt.ExpiredSignatureError:
                return ({"code": "token_expired",
                        "description": "token is expired"}, 401)
            except jwt.JWTClaimsError:
                return ({"code": "invalid_claims",
                        "description": "Incorrect claims. Please check the audience and issuer."}, 401)
            except Exception:
                return ({"code": "invalid_header",
                        "description": "Unable to parse authentication token."}, 400)


            _app_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        return ({"code": "invalid_header",
                "description": "Unable to find appropriate key"}, 400)
    return decorated


def get_extension_access_token():

    payload = "{\"client_id\":\"NJh7jJsES1ymojwuBodeZJCzT867UNiu\",\"client_secret\":\"sZXs4dsAOzJlnJgLVXEyHQ5XLZ4TP-zlNeUs54nZN1tRPFL-UsFmCZQC6FFHRXtr\",\"audience\":\"urn:auth0-authz-api\",\"grant_type\":\"client_credentials\"}"

    headers = {'content-type': "application/json"}
    r = requests.post("https://ekryp.auth0.com/oauth/token", data=payload, headers=headers)
    response_json = r.json()
    return response_json['access_token']


class Permission(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(Permission, self).__init__()

    @requires_auth
    def get(self):
        extension_access_token = get_extension_access_token()
        headers = {
            'Authorization': 'Bearer {0}'.format(extension_access_token),
            'content-type': 'application/json',
        }
        routes = 'permissions'
        ext_url = Configuration.AUTH0_EXTERNAL_API + routes
        response = requests.get(ext_url, headers=headers)
        all_applications_permissions = response.json().get('permissions')
        permissions = []

        def get_related_application_permission(all_applications_permissions):

            for each_permission in all_applications_permissions:
                if each_permission.get('applicationId') == Configuration.AUTH0_CLIENT_ID:
                    permissions.append(each_permission)


        get_related_application_permission(all_applications_permissions)

        return jsonify(permissions=permissions, http_status_code=200)

    def options(self):
        pass


class Roles(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(Roles, self).__init__()

    @requires_auth
    def post(self):

        ''' Create a New Role Functionality '''
        def create_request_parser():
            self.parser = reqparse.RequestParser()
            self.parser.add_argument('role_name', required=True, location='form')
            self.parser.add_argument('role_description', required=True , location='form')
            self.parser.add_argument('role_permission', required=True, location='form')
            return self.parser

        create_request_parser()
        args = self.parser.parse_args()
        extension_access_token = get_extension_access_token()
        permission_ids = []
        permission_object = args['role_permission']
        permission_object=json.loads(permission_object)
        for each_permission in permission_object:
            permission_ids.append(each_permission.get('_id'))

        headers = {
            'Authorization': 'Bearer {0}'.format(extension_access_token),
            'content-type': 'application/json',
        }
        data = {"name": args['role_name'], "description": args['role_description'],
                "applicationType": "client", "applicationId": Configuration.AUTH0_CLIENT_ID,
                "permissions": permission_ids}
        data = json.dumps(data)
        routes = 'roles'
        ext_url = Configuration.AUTH0_EXTERNAL_API + routes
        response = requests.post(ext_url, headers=headers, data=data)
        if response.status_code != 200:
            # 200 means The role was created, other than 200 means exception occured
            # sample error codes are
            # 403	Insufficient scope, expected any of: create:role
            # 400	The role already exists.
            return jsonify(msg=response.json().get('message'), http_status_code=500)
        return jsonify(msg=" Role Created Successfully", http_status_code=200)

    @requires_auth
    def put(self):

        def create_request_parser():
            self.parser = reqparse.RequestParser()
            self.parser.add_argument('checkedRoles', action='append', required=True, location='form')
            self.parser.add_argument('userId', required=True, location='form')
            return self.parser

        create_request_parser()
        args = self.parser.parse_args()

        extension_access_token = get_extension_access_token()
        ext_url = "https://ekryp.us.webtask.io/adf6e2f2b84784b57522e3b19dfc9201/api/users/" + args['userId'] + "/roles"
        roles = requests.get(ext_url, data=None, headers={'authorization': "Bearer " + extension_access_token})
        rolesJson = roles.json()

        existing_roles = []
        for role in rolesJson:
            existing_roles.append(role['_id'])

        ext_url = "https://ekryp.us.webtask.io/adf6e2f2b84784b57522e3b19dfc9201/api/users/" + args['userId'] + "/roles"
        delete_existing_roles = requests.delete(ext_url, json=existing_roles,
                                                headers={'authorization': "Bearer " + extension_access_token})

        ext_url = "https://ekryp.us.webtask.io/adf6e2f2b84784b57522e3b19dfc9201/api/users/" + args['userId'] + "/roles"
        add_new_roles = requests.patch(ext_url, json=args['checkedRoles'],
                                       headers={'authorization': "Bearer " + extension_access_token})

        ext_url = "https://ekryp.us.webtask.io/adf6e2f2b84784b57522e3b19dfc9201/api/users/" + args['userId'] + "/roles"
        roles = requests.get(ext_url, data=None, headers={'authorization': "Bearer " + extension_access_token})
        updated_roles = roles.json()

        return  jsonify(msg="Roles Updated Sucessfully", http_status_code=200)

    def options(self):
        pass


class Role(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(Role, self).__init__()

    @requires_auth
    def put(self):
        ''' Modify a role Functionality '''
        def create_request_parser():
            self.parser = reqparse.RequestParser()
            self.parser.add_argument('role_description', required=True, location='form')
            self.parser.add_argument('role_id', required=True, location='form')
            self.parser.add_argument('role_description', required=True, location='form')
            self.parser.add_argument('role_permission', required=True, location='form')
            self.parser.add_argument('role_name', required=True, location='form')
            return self.parser

        create_request_parser()
        args = self.parser.parse_args()
        permission_ids = []
        permission_object = args['role_permission']
        permission_object=json.loads(permission_object)
        for each_permission in permission_object:
            permission_ids.append(each_permission.get('_id'))
        extension_access_token = get_extension_access_token()
        headers = {
            'Authorization': 'Bearer {0}'.format(extension_access_token),
            'content-type': 'application/json',
        }
        routes = 'roles' + '/' + args['role_id']
        data = {"name": args['role_name'], "description": args['role_description'],
                "applicationType": "client", "applicationId": Configuration.AUTH0_CLIENT_ID,
                "permissions": permission_ids}
        data = json.dumps(data)
        ext_url = Configuration.AUTH0_EXTERNAL_API + routes
        response = requests.put(ext_url, headers=headers, data=data)
        return response.json()

    @requires_auth
    def delete(self):
        ''' Delete a role Functionality '''
        def create_request_parser():
            self.parser = reqparse.RequestParser()
            self.parser.add_argument('role_id', required=True, location='args')
            return self.parser

        create_request_parser()
        args = self.parser.parse_args()
        extension_access_token = get_extension_access_token()
        headers = {
            'Authorization': 'Bearer {0}'.format(extension_access_token),
            'content-type': 'application/json',
        }
        role_id = args['role_id']
        #check user assigned to that role,do not delete if user is attached to that role

        def linked_user_to_role():
            routes = 'roles'
            ext_url = Configuration.AUTH0_EXTERNAL_API + routes
            response = requests.get(ext_url, headers=headers)
            all_roles = response.json()['roles']  # Returns all roles across all applications
            application_specific_role = []
            for role in all_roles:
                if Configuration.AUTH0_CLIENT_ID == role.get('applicationId'):
                    application_specific_role.append(role)

            for role in application_specific_role:
                if role_id == role.get("_id"):
                    if 'users' in role.keys():
                        if len(role.get('users')) > 0:
                            return True
                        else:
                            return False
                    else:
                        return False

        is_linked = linked_user_to_role()
        if is_linked:
            return jsonify(msg="Role Can'b be Deleted,As Users are assigned to role", http_status_code=400)
        else:
            routes = 'roles' + '/' + role_id
            ext_url = Configuration.AUTH0_EXTERNAL_API + routes
            response = requests.delete(ext_url, headers=headers)
            return jsonify(msg="Role Deleted", http_status_code=200)

    def options(self):
        pass
