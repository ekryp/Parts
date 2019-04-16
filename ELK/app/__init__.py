import logging
import platform
import string
from importlib import import_module
from logging.handlers import RotatingFileHandler

from flask import Blueprint, Flask
from flask_compress import Compress
from flask_jwt import JWT
from flask_restful import Api
from flask_cors import CORS

compress = Compress()
API_URL_PREFIX = '/api'
api_blueprint = Blueprint('api', __name__)

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

api = Api(
    app=api_blueprint,
    prefix = API_URL_PREFIX,
    catch_all_404s=True
)

app.config['SECRET_KEY'] = 'secret'

# jwt = JWT(app, authenticate, identity)
compress.init_app(app)

from app.devtrack.devtrack import DevTrackData


api.add_resource(DevTrackData, '/getDevTrackData', endpoint='getDevTrackData')

app.register_blueprint(api_blueprint)
api.init_app(app)