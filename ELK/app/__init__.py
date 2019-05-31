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

from app.devtrack.devtrack import DevTrackData,DevTrackPhrasePrefix
from app.fsb.fsb import FSB
from app.releasenotes.releasenotes import ReleaseNotes
from app.Testplan.testplan import TestPlan,TestPlanPhrase
from app.Keywords.keywords import GetMLKeyWords
from app.mop.mop import MOP,MopPhrase
from app.technotes.technote import TechNotes,TechNotePhrase

api.add_resource(DevTrackData, '/getDevTrackData', endpoint='getDevTrackData')
api.add_resource(DevTrackPhrasePrefix, '/get_devtrack_data_preffix', endpoint='get_devtrack_data_preffix')
api.add_resource(GetMLKeyWords, '/get_ml_keywords', endpoint='get_ml_keywords')
api.add_resource(TestPlan, '/get_test_plan', endpoint='get_test_plan')
api.add_resource(TestPlan, '/delete_testplan', endpoint='delete_testplan')
api.add_resource(TestPlanPhrase, '/get_all_test_plan', endpoint='get_all_test_plan')
api.add_resource(ReleaseNotes, '/get_release_notes', endpoint='get_release_notes')
api.add_resource(FSB, '/get_fsb', endpoint='get_fsb')
api.add_resource(MOP, '/get_mop', endpoint='get_mop')
api.add_resource(MOP, '/delete_mop', endpoint='delete_mop')
api.add_resource(MopPhrase, '/get_all_mop', endpoint='get_all_mop')
api.add_resource(TechNotes, '/get_technotes', endpoint='get_technotes')
api.add_resource(TechNotePhrase, '/get_all_technotes', endpoint='get_all_technotes')

app.register_blueprint(api_blueprint)
api.init_app(app)