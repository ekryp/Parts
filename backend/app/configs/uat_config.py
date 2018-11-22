from app.configs.base_config import BaseConfig


class Configuration(BaseConfig):
    DEBUG = True

    CUSTOMER_DATA_DB_URI = "mysql+cymysql://root:ekryp@10.138.1.12/arca_care_data_db_uat"
    EKRYP_DATA_DB_URI = "mysql+cymysql://root:ekryp@10.138.1.12/ekryp_core_test"
    EKRYP_USER_DB_URI = "mysql+cymysql://root:ekryp@10.138.1.12/ekryp_staging"
    ML_DB_URI = "mysql+cymysql://root:ekryp@10.138.1.12/ml_staging"
    PARTS_DB_URI = "mysql+cymysql://root:ekryp@10.138.1.12/parts_data"

    # EKRYP_DATA_DB_URI = "mysql+cymysql://ekrypdbuser:EKryPUs3R6@arcadata.cxw9irlmjfr2.us-east-1.rds.amazonaws.com/ekryp_data_uat"
    # EKRYP_USER_DB_URI = "mysql+cymysql://ekrypdbuser:EKryPUs3R6@arcadata.cxw9irlmjfr2.us-east-1.rds.amazonaws.com/ekryp_prod_demo"
    # ML_DB_URI = "mysql+cymysql://ekrypdbuser:EKryPUs3R6@arcadata.cxw9irlmjfr2.us-east-1.rds.amazonaws.com/ml_demo"


    SECRET_KEY = "stuff"
    SERVER_NAME = None
    LOG_FILENAME = "pyservices_application.log"
    AUTH0_DOMAIN = "ekryp.auth0.com"
    AUTH0_CLIENT_ID = "3tumfGf9w7BPeHzWrLMcvcHYg5MMQUiY"
    AUTH0_CLIENT_SECRET_KEY = "uKAETloe1wlypz2e8Th2-qlbeciA4A7KnI69eresCyrngPmn1xp1iSzN_LY7iOKj"
    AUTH0_API_AUDIENCE = "http://34.233.126.29:5000/api/v1/"
