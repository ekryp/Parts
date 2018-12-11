import os
from dateutil import tz

class BaseConfig(object):
    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
    LOG_FORMAT = '%(asctime)s:%(levelname)s:%(name)s:%(message)s'
    LOG_LEVEL = 'DEBUG'
    DRUID_TZ = tz.tzutc()
    DB_MODELS_IMPORTS =('app.models.druid_column','app.models.druid_datasource','app.models.druid_cluster','app.models.ekryp_user','app.models.ekryp_partner','app.models.datasource_partner')

    TEMP_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'temp_files')

    MAIL_GUN_API_URL = 'https://api.mailgun.net/v3/noreply.ekryp.com/'
    MAIL_GUN_API_KEY = 'key-06a2334ec7daa13d562564d303582d63'
    CLIENT_SECRET_FILE = 'client_secret.json'
    prospect_id = ''