from app.configs.base_config import BaseConfig


class Configuration(BaseConfig):
    DEBUG = True

    EKRYP_DATA_DB_URI = "mysql+cymysql://root:admin@localhost/ekryp_core_test"

    EKRYP_USER_DB_URI = "mysql+cymysql://root:admin@localhost/ekryp_local"

    PROSPECT_DB_URL = "mysql+cymysql://root:admin@localhost/ekryp_prospect_db"

    AIRFLOW_DB_URL = "mysql+cymysql://root:Ekryp#1234@35.199.174.191/ekryp_challenge"

    DRUID_HOST = 'http://10.43.12.29:8090/druid/indexer/v1/task'
    MYSQL_USER = "root"
    MYSQL_HOST = "localhost"
    MYSQL_PWD = "admin"
    MYSQL_DB = "ekryp_local"

    BASE_DIR = r"C:\Users\GS-1731\Desktop"
    TSV_DEST = r"C:\Users\GS-1731\Desktop\tsvs"
    DRUID_DRIVE = r"C:\Users\GS-1731\Desktop\tsvs"

    AIRFLOW_HOST = '10.138.1.13'
    AIRFLOW_PORT = '8080'

    SECRET_KEY = "stuff"
    SERVER_NAME = None
    LOG_FILENAME = "pyservices_application.log"
    AUTH0_DOMAIN = "ekryp.auth0.com"
    AUTH0_CLIENT_ID = "3tumfGf9w7BPeHzWrLMcvcHYg5MMQUiY"
    AUTH0_CLIENT_SECRET_KEY = "uKAETloe1wlypz2e8Th2-qlbeciA4A7KnI69eresCyrngPmn1xp1iSzN_LY7iOKj"
    AUTH0_API_AUDIENCE = "http://localhost:5000/api/v1/"
