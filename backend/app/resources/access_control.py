from flask import jsonify, request
from flask_restful import Resource
from flask_restful import reqparse
from app import Configuration
from app.auth.authorization import requires_auth, get_extension_access_token
from auth0.v3.authentication import GetToken
import requests
import json
from app.tasks import sendEmailNotificatio


class ResetPassword(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('new_password', type=str, required=False, help='not Provided', location='form')
        self.reqparse.add_argument('user_id', type=str, required=False, help='not Provided', location='form')
        super(ResetPassword, self).__init__()

    @requires_auth
    def post(self):
       
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

            if response.json().get('message') == "PasswordHistoryError: Password has previously been used":
                return jsonify(msg="New Password Cannot be the same as previously used last 5 passwords",
                               http_status_code=400)

            return jsonify(msg=response.json().get('message'), http_status_code=400)
        else:
            return jsonify(msg="Password changed Sucessfully", http_status_code=200)

    def options(self):
        pass


class Role(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(Role, self).__init__()

    @requires_auth
    def get(self):
        extension_access_token = get_extension_access_token()
        headers = {
            'Authorization': 'Bearer {0}'.format(extension_access_token),
            'content-type': 'application/json',
        }
        routes = 'roles'
        ext_url = Configuration.AUTH0_EXTERNAL_API + routes
        response = requests.get(ext_url, headers=headers)
        all_roles = response.json()['roles']  # Returns all roles across all applications
        application_specific_role = []
        for role in all_roles:
            if Configuration.AUTH0_CLIENT_ID == role.get('applicationId'):
                application_specific_role.append(role)
        return application_specific_role

    @requires_auth
    def post(self):
        extension_access_token = get_extension_access_token()
        headers = {
            'Authorization': 'Bearer {0}'.format(extension_access_token),
            'content-type': 'application/json',
        }

        routes = 'permissions'
        ext_url = Configuration.AUTH0_EXTERNAL_API + routes
        permissions = requests.get(ext_url, headers=headers).json()['permissions']
        admin_permissions_for_application = []
        for each_permission in permissions:
            if Configuration.AUTH0_CLIENT_ID == each_permission.get('applicationId'):
                admin_permissions_for_application.append(each_permission.get('_id'))

        data = {"name": "Admin Role", "description": "Admin having all permissions",
                "applicationType": "client", "applicationId": Configuration.AUTH0_CLIENT_ID,
                "permissions": admin_permissions_for_application,
                }
        data = json.dumps(data)
        routes = 'roles'
        ext_url = Configuration.AUTH0_EXTERNAL_API + routes
        response = requests.post(ext_url, headers=headers, data=data)
        return response.json()

    @requires_auth
    def delete(self):
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

        # check user assigned to that role,do not delete if user is attached to that role
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

    @requires_auth
    def put(self):

        def create_request_parser():
            self.parser = reqparse.RequestParser()
            self.parser.add_argument('role_description', required=True, location='form')
            self.parser.add_argument('role_id', required=True, location='form')
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
        
        return jsonify(msg=" Role Details Updated Successfully", http_status_code=200)

    def options(self):
        pass


class User(Resource):

    def __init__(self):
        super(User, self).__init__()

    @requires_auth
    def get(self):

        def create_request_parser():
            self.parser = reqparse.RequestParser()
            return self.parser
        create_request_parser()
        args = self.parser.parse_args()
        extension_access_token = get_extension_access_token()
        headers = {
            'Authorization': 'Bearer {0}'.format(extension_access_token),
            'content-type': 'application/json',
        }

        routes = 'groups' + '/' + Configuration.AUTH0_INFINERA_GROUP_ID + '/' + 'members'
        ext_url = Configuration.AUTH0_EXTERNAL_API + routes
        response = requests.get(ext_url, headers=headers)
        total = response.json().get('total')
        print("total users are: {0}".format(str(total)))
        users = []
        if total > 25:
            '''
            The Auth0 APi sends only 25 User data in one go,Here we have more than 25 users
            So we have to call auth0 APi multiple times to fetch all users data.
            Lets say we have 28 users
            So we will call auth0 API twice
            groups/GROUP_ID/members?per_page=25&page=1   This will give first 25
            groups/GROUP_ID/members?per_page=25&page=2   This will give remaining 3
            
            '''

            from math import ceil
            pages = ceil(total/25)
            pages = list(range(pages))
            for page in pages:
                print("Paginating page {0}:".format(str(page+1)))
                per_page = 25
                routes = 'groups' + '/' + Configuration.AUTH0_INFINERA_GROUP_ID + '/' + 'members' + '?per_page=' + str(per_page) +'&page=' + str(page + 1)
                print(routes)
                ext_url = Configuration.AUTH0_EXTERNAL_API + routes
                response = requests.get(ext_url, headers=headers)
                for each_user in response.json().get('users'):
                    users_dict = {}
                    users_dict['email'] = each_user.get('email')
                    users_dict['username'] = each_user.get('username', "NA")
                    headers = {
                        'Authorization': 'Bearer {0}'.format(extension_access_token),
                        'content-type': 'application/json',
                    }

                    routes = 'users' + '/' + each_user.get('user_id') + '/' + 'roles'
                    ext_url = Configuration.AUTH0_EXTERNAL_API + routes
                    response = requests.get(ext_url, headers=headers)
                    application_specific_role = []
                    for role in response.json():
                        if Configuration.AUTH0_CLIENT_ID == role.get('applicationId'):
                            application_specific_role.append(role)

                    users_dict['user_id'] = each_user.get('user_id')
                    users_dict['roles'] = application_specific_role
                    print(users_dict.get('username'),users_dict.get('email'))
                    users.append(users_dict)

        else:

            for each_user in response.json().get('users'):
                users_dict = {}
                users_dict['email'] = each_user.get('email')
                users_dict['username'] = each_user.get('username', "NA")
                headers = {
                'Authorization': 'Bearer {0}'.format(extension_access_token),
                'content-type': 'application/json',
                }

                routes = 'users' + '/' + each_user.get('user_id') + '/' + 'roles'
                ext_url = Configuration.AUTH0_EXTERNAL_API + routes
                response = requests.get(ext_url, headers=headers)
                application_specific_role = []
                for role in response.json():
                    if Configuration.AUTH0_CLIENT_ID == role.get('applicationId'):
                        application_specific_role.append(role)

                users_dict['user_id'] = each_user.get('user_id')
                users_dict['roles']=application_specific_role
                users.append(users_dict)

        return users

    @requires_auth
    def post(self):
        def create_request_parser():
            self.parser = reqparse.RequestParser()
            self.parser.add_argument('email', required=True, location='json')
            self.parser.add_argument('connection', required=True, default='db-users', location='json')
            self.parser.add_argument('password', required=True, location='json')
            self.parser.add_argument('username', required=True, location='json')
            return self.parser

        create_request_parser()
        args = self.parser.parse_args()
        data = request.get_json()
        non_interactive_client_id = Configuration.AUTH0_CLIENT_ID
        non_interactive_client_secret = Configuration.AUTH0_CLIENT_SECRET_KEY

        get_token = GetToken(Configuration.AUTH0_DOMAIN)
        token = get_token.client_credentials(non_interactive_client_id,
                                             non_interactive_client_secret,
                                             'https://{}/api/v2/'.format(Configuration.AUTH0_DOMAIN))
        mgmt_api_token = token['access_token']
        routes = 'users'
        ext_url = Configuration.AUTH0_MGMT_API + routes

        # Below Code is for mapping new user with group

        group_name = Configuration.AUTH0_INFINERA_GROUP_NAME
        data1 = {
            "user_metadata": {
                "first_name": request.get_json().get('username')
            },
            "app_metadata": {"authorization": {
                    "groups": group_name,
                    "roles": [],
                "permissions": []
                                            }
            }
        }
        data.update(data1)
        data = json.dumps(data)
        headers = {
            'Authorization': 'Bearer {0}'.format(mgmt_api_token),
            'content-type': 'application/json',
        }
        # This Creates a new user
        response = requests.post(ext_url, headers=headers, data=data)
        if response.status_code != 201:
            # 201 means The user was created, other than 201 means exception occured
            # sample error codes are
            # 403	Insufficient scope, expected any of: create:users
            # 409	The user already exists.
            return jsonify(msg=response.json().get('message'), http_status_code=500)

        group_id = Configuration.AUTH0_INFINERA_GROUP_ID
        extension_access_token = get_extension_access_token()
        headers = {
            'Authorization': 'Bearer {0}'.format(extension_access_token),
            'content-type': 'application/json',
        }
        routes = 'groups' + '/' + group_id + '/' + 'members'
        ext_url = Configuration.AUTH0_EXTERNAL_API + routes
        data = [response.json().get('user_id')]
        data = json.dumps(data)
        res = requests.patch(ext_url, headers=headers, data=data)
        subject = "Infinera Access"
        message = "New User {0} created & password is {1}".format(request.get_json().get('username'),
                                                                  request.get_json().get('password'))
        to_email = request.get_json().get('email')
        try:
            sendEmailNotificatio(to_email, subject, message)
        except:
            pass
            # ignore error msg from mailgun

        return jsonify(msg="User Created Successfully", user_id=response.json().get('user_id'), http_status_code=200)

    @requires_auth
    def delete(self):
        def create_request_parser():
            self.parser = reqparse.RequestParser()
            self.parser.add_argument('user_id', required=True, location='args')
            return self.parser

        create_request_parser()
        args = self.parser.parse_args()
        non_interactive_client_id = Configuration.AUTH0_CLIENT_ID
        non_interactive_client_secret = Configuration.AUTH0_CLIENT_SECRET_KEY

        get_token = GetToken(Configuration.AUTH0_DOMAIN)
        token = get_token.client_credentials(non_interactive_client_id,
                                             non_interactive_client_secret,
                                             'https://{}/api/v2/'.format(Configuration.AUTH0_DOMAIN))
        mgmt_api_token = token['access_token']
        routes = 'users' + '/' + args['user_id']
        ext_url = Configuration.AUTH0_MGMT_API + routes
        headers = {
            'Authorization': 'Bearer {0}'.format(mgmt_api_token),
            'content-type': 'application/json',
        }
        response = requests.delete(ext_url, headers=headers)

        # Below Code removes mapping of group id with User.
        group_id = Configuration.AUTH0_INFINERA_GROUP_ID
        extension_access_token = get_extension_access_token()
        headers = {
            'Authorization': 'Bearer {0}'.format(extension_access_token),
            'content-type': 'application/json',
        }
        routes = 'groups' + '/' + group_id + '/' + 'members'
        ext_url = Configuration.AUTH0_EXTERNAL_API + routes
        data = [args['user_id']]
        data = json.dumps(data)
        res = requests.delete(ext_url, headers=headers, data=data)
        return jsonify(msg="User Deleted", http_status_code=200)

    def options(self):
        pass


class User_Role(Resource):

    def __init__(self):
        super(User_Role, self).__init__()

    @requires_auth
    def get(self):
        def create_request_parser():
            self.parser = reqparse.RequestParser()
            self.parser.add_argument('user_id', required=True, location='args')
            return self.parser

        create_request_parser()
        args = self.parser.parse_args()
        extension_access_token = get_extension_access_token()
        headers = {
            'Authorization': 'Bearer {0}'.format(extension_access_token),
            'content-type': 'application/json',
        }

        routes = 'users' + '/' + args['user_id'] + '/' + 'roles'
        ext_url = Configuration.AUTH0_EXTERNAL_API + routes
        response = requests.get(ext_url, headers=headers)
        application_specific_role = []
        for role in response.json():
            if Configuration.AUTH0_CLIENT_ID == role.get('applicationId'):
                application_specific_role.append(role)
        return application_specific_role

    def options(self):
        pass

