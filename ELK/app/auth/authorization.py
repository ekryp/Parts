import urllib

import requests
from flask import request, jsonify
from flask import _app_ctx_stack
import json
from flask_restful import Resource, reqparse

from jose import jwt
from six.moves.urllib.request import urlopen
from functools import wraps


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

        jsonurl = urlopen("https://ekryp.auth0.com/.well-known/jwks.json")
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
                    audience="https://prod-services.ekryp.com/api/v1/",
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
