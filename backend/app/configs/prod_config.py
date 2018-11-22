from app.configs.base_config import BaseConfig


class Configuration(BaseConfig):
    DEBUG = True

    EKRYP_DATA_DB_URI = "mysql+cymysql://ashish:Ekryp#1234@35.199.174.191/ekryp_core_prospect"

    EKRYP_USER_DB_URI = "mysql+cymysql://ashish:Ekryp#1234@35.199.174.191/ekryp_prospect"

    PROSPECT_DB_URL = "mysql+cymysql://ashish:Ekryp#1234@35.199.174.191/ekryp_prospect_db"
	
    AIRFLOW_DB_URL = "mysql+cymysql://ashish:Ekryp#1234@35.199.174.191/ekryp_challenge"

    DRUID_HOST='http://10.138.1.14:8090/druid/indexer/v1/task'
    MYSQL_USER="root"
    MYSQL_HOST="35.199.174.191"
    MYSQL_PWD="Ekryp#1234"
    MYSQL_DB="ekryp_core_prospect"

    AIRFLOW_HOST = '10.138.1.13'
    AIRFLOW_PORT = '8080'

    BASE_DIR = '/home/attachedDisk/google-cloud-storage/'
    TSV_DEST = '/d01/google-cloud-storage/tsvs'
    DRUID_DRIVE = '/home/attachedDisk/google-cloud-storage/tsvs'

    SECRET_KEY = "stuff"
    SERVER_NAME = None
    LOG_FILENAME = "pyservices_application.log"
    AUTH0_DOMAIN = "ekryp.auth0.com"
    AUTH0_CLIENT_ID = "bMaDtUC3cScPcrex943NVOqhPHsK20mt"
    AUTH0_CLIENT_SECRET_KEY = "PSuFfYPt6tK2ltj2sYiatgL_aSkzOEWOZrJJGUZ6X9w74xAelDTtCnrpWIzYJHPO"
    AUTH0_API_AUDIENCE = "https://prod-services/api/v1/"

