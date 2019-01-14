import logging
import platform
import string
from importlib import import_module
from logging.handlers import RotatingFileHandler

# from flask_security import SQLAlchemyUserDatastore
# from flask_security import Security
from flask import Blueprint, Flask
from flask_compress import Compress
from flask_jwt import JWT
from flask_restful import Api
from flask_restful.utils import cors

from app.configs import Configuration
from app.models.basemodel import db
from app.models.ekryp_role import Role
from app.models.ekryp_user import User
from app.models.ekryp_user import User
from app.resources.users import authenticate, identity
# import flask_profiler
from .cache import cache

compress = Compress()

API_VERSION = 1
API_URL_PREFIX = '/api/v%s' % API_VERSION
api_blueprint = Blueprint('api', __name__)


ALLOWED_EXTENSIONS = set(['csv', 'xlsx'])
fileSaveName = 'batch'
models = {}
printable = set(string.printable)

#from flask_uploads import UploadSet, configure_uploads, DATA
from flask_uploads import configure_uploads
app = Flask(__name__)
#from app.resources.partners import csvs
from flask_uploads import UploadSet, DATA, DOCUMENTS, IMAGES, TEXT
csvs = UploadSet('csv', DATA)
mytext = UploadSet('text', TEXT)
excel = UploadSet('excel', DOCUMENTS)
images = UploadSet('image', IMAGES)

if platform.system() == 'Windows':
    app.config['UPLOADED_CSV_DEST'] = 'static\csvs'
    app.config['UPLOADED_JSON_DEST'] = 'jstatic\sons'
    app.config['UPLOADED_SQLS_DEST'] = 'static\sqls'
    app.config['UPLOADED_EXCEL_DEST'] = 'static\excel'
    app.config['UPLOADED_IMAGE_DEST'] = 'static\image'
else:
    app.config['UPLOADED_CSV_DEST'] = 'static/'
    app.config['UPLOADED_TEXT_DEST'] = 'static/'
    app.config['UPLOADED_SQLS_DEST'] = 'static/'
    app.config['UPLOADED_EXCEL_DEST'] = 'static/'
    app.config['UPLOADED_IMAGE_DEST'] = 'static/'

configure_uploads(app, csvs)
configure_uploads(app, images)
configure_uploads(app, mytext)
configure_uploads(app, excel)
cache.init_app(app, config={'CACHE_TYPE': 'simple'})

app.config.from_object(Configuration)

formatter = logging.Formatter(app.config.get('LOG_FORMAT'))
handler = RotatingFileHandler(app.config.get('LOG_FILENAME'), maxBytes=10000000, backupCount=5)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
app.logger.addHandler(handler)



api = Api(
    app=api_blueprint,
    prefix = API_URL_PREFIX,
    catch_all_404s=True
)
db = db

api.decorators = [
    cors.crossdomain(
        origin='*',
        methods=['GET', 'PUT', 'POST', 'DELETE', 'OPTIONS'],
        headers=['authorization', 'content-type'],
        attach_to_all=True,
        automatic_options=True
        )
    ]

with app.app_context():
    for module in app.config.get('DB_MODELS_IMPORTS', list()):
        import_module(module)

app.config['SECRET_KEY'] = 'secret'

jwt = JWT(app, authenticate, identity)

app.config.update(
    CELERY_BROKER_URL='amqp://root1:root1@localhost:5672/demohost',
    CELERY_RESULT_BACKEND='amqp://root1:root1@localhost:5672/demohost',
    CELERYBEAT_SCHEDULER='app.tasks.sqlalchemy_scheduler:DatabaseScheduler',
    FILE_SAVE_NAME=fileSaveName,
    ALLOWED_EXTENSIONS=ALLOWED_EXTENSIONS
)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

db.init_app(app)
compress.init_app(app)
DRUID_TZ = app.config.get('DRUID_TZ')
from app.resources.partners import UploadCSV


from app.resources.users import  Callback, Logout
from app.resources.prospects import ProspectsInfo,SetProspectDone,TriggerDag,ExperimentDetails
from app.resources.infinera import GetSparePartAnalysis,PostSparePartAnalysis,Reference,GetReference,DefaultReference,GetReferenceById,GetstepsAllUsers,\
    GetstepsforSpecificRequest, GetSummaryforSpecificRequest,GetDashboardRequestCount,\
    GetMainDashboardCount, GetPieChart, GetTopPons, GetTopDepots, GetTopCustomer, GetTopExtended,\
    GetGrossforSpecificRequest, GetCurrentInventory, GetCurrentNet, GetCurrentIB, GetLatLon, GetAnalysisName, \
    GetErrorRecords

from app.resources.reference import UploadParts, UploadDepot, UploadNode, UploadHighSpare,\
    UploadMisnomer


api.add_resource(Callback, '/token')
api.add_resource(Logout, '/logout')


api.add_resource(ProspectsInfo, '/fetch_prospects', endpoint='fetch_prospects')
api.add_resource(SetProspectDone, '/set_prospects', endpoint='set_prospects')
api.add_resource(UploadCSV, '/upload_csv', endpoint='upload_csv')
api.add_resource(TriggerDag, '/trigger_dag', endpoint='trigger_dag')
api.add_resource(ExperimentDetails, '/experiment_details', endpoint='experiment_details')
api.add_resource(GetSparePartAnalysis, '/get_spare_part_analysis', endpoint='get_spare_part_analysis')
api.add_resource(PostSparePartAnalysis, '/post_spare_part_analysis', endpoint='post_spare_part_analysis')
api.add_resource(Reference, '/reference', endpoint='/reference')
api.add_resource(GetReference, '/getreference', endpoint='/getreference')
api.add_resource(GetReferenceById, '/getreferencebyId', endpoint='/getreferencebyId')
api.add_resource(DefaultReference,'/reference/default',endpoint='/reference/default')
api.add_resource(GetstepsAllUsers, '/get_steps_all_users', endpoint='get_steps_all_users')
api.add_resource(GetstepsforSpecificRequest, '/get_steps_specific_request', endpoint='get_steps_specific_request')
api.add_resource(GetSummaryforSpecificRequest, '/get_summary_specific_request', endpoint='get_summary_specific_request')
api.add_resource(GetCurrentInventory, '/get_current_inventory_specific_request', endpoint='get_current_inventory_specific_request')
api.add_resource(GetCurrentNet, '/get_current_net_specific_request', endpoint='get_current_net_specific_request')
api.add_resource(GetCurrentIB, '/get_current_ib_specific_request', endpoint='get_current_ib_specific_request')
api.add_resource(GetAnalysisName, '/get_analysis_name', endpoint='get_analysis_name')
api.add_resource(GetErrorRecords, '/get_error_records', endpoint='get_error_records')
api.add_resource(GetDashboardRequestCount, '/get_dashboard_request_count', endpoint='get_dashboard_request_count')
api.add_resource(GetGrossforSpecificRequest, '/get_gross_specific_request', endpoint='get_gross_specific_request')
api.add_resource(GetMainDashboardCount, '/get_main_dashboard_count', endpoint='get_main_dashboard_count')
api.add_resource(GetPieChart, '/get_pie_chart', endpoint='get_pie_chart')
api.add_resource(GetTopPons, '/get_top_pons', endpoint='get_top_pons')
api.add_resource(GetTopDepots, '/get_top_depots', endpoint='get_top_depots')
api.add_resource(GetTopCustomer, '/get_top_customers', endpoint='get_top_customers')
api.add_resource(GetTopExtended, '/get_top_extended', endpoint='get_top_extended')
api.add_resource(GetLatLon, '/get_lat_lon', endpoint='get_lat_lon')
api.add_resource(UploadParts, '/post_parts', endpoint='post_parts')
api.add_resource(UploadDepot, '/post_depot', endpoint='post_depot')
api.add_resource(UploadNode, '/post_node', endpoint='post_node')
api.add_resource(UploadHighSpare, '/post_high_spare', endpoint='post_high_spare')
api.add_resource(UploadMisnomer, '/post_misnomer', endpoint='post_misnomer')

app.register_blueprint(api_blueprint)
api.init_app(app)

