from app.configs.base_config import BaseConfig
import os


class Configuration(BaseConfig):
    DEBUG = True

    EKRYP_DATA_DB_URI = "mysql+cymysql://ashish:Ekryp#1234@35.199.174.191/ekryp_core_prospect"

    EKRYP_USER_DB_URI = "mysql+cymysql://ashish:Ekryp#1234@35.199.174.191/ekryp_prospect"

    PROSPECT_DB_URL = "mysql+cymysql://ashish:Ekryp#1234@35.199.174.191/ekryp_prospect_db"
	
    AIRFLOW_DB_URL = "mysql+cymysql://ashish:Ekryp#1234@35.199.174.191/ekryp_challenge"

    INFINERA_DB_URL = "mysql+cymysql://root:tang3456@35.197.23.168/infinera"

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
    AUTH0_CLIENT_ID = "NJh7jJsES1ymojwuBodeZJCzT867UNiu"
    AUTH0_CLIENT_SECRET_KEY = "sZXs4dsAOzJlnJgLVXEyHQ5XLZ4TP-zlNeUs54nZN1tRPFL-UsFmCZQC6FFHRXtr"
    AUTH0_API_AUDIENCE = "https://prod-services.ekryp.com/api/v1/"
    AUTH0_MGMT_API = 'https://ekryp.auth0.com/api/v2/'
    AUTH0_EXTERNAL_API = "https://ekryp.us.webtask.io/adf6e2f2b84784b57522e3b19dfc9201/api/"
    AUTH0_INFINERA_GROUP_ID = 'b84a112a-259b-46ec-afb4-4e4ca2c18250'
    AUTH0_INFINERA_GROUP_NAME = 'infinera'
    FLOWER_HOST = "flower"

    DEBUG = True
    ECLIPSE_DATA_DB_URI = "mysql+cymysql://root:tang3456@35.197.23.168/infinera"
    BASE_DIR = r'/data'

    ssl_args = {'ssl': {'cert': '/data/client-cert.pem', 'key': '/data/client-key.pem',
                        'ca': '/data/server-ca.pem'}}

    net_depot = os.path.join(BASE_DIR, 'net_depot.csv')
    DNA_BOM = os.path.join(BASE_DIR, 'DNA_BOM_table.csv')
    MTBF_BOM = os.path.join(BASE_DIR, 'MTBF_BOM.csv.csv')
    gross_quantity_bom = os.path.join(BASE_DIR, 'gross_quantity_bom.csv')
    summary_output = os.path.join(BASE_DIR, 'summaryoutput.csv')
    bom_table = os.path.join(BASE_DIR, 'bomcal.csv')
    mtbf_bom_table = os.path.join(BASE_DIR, 'mtbfbom.csv')
    depot_master_file_location = os.path.join(BASE_DIR, '5-Depot Master.xlsx')
    sap_export_file_location = os.path.join(BASE_DIR, '3-SAPexport.XLSX')
    sap_export = os.path.join(BASE_DIR, '3-SAPexport.XLSX')
    spms_reference_file_location = os.path.join(BASE_DIR, '4-SPMS_Reference_Data.xlsx')
    standard_cost_file_location = os.path.join(BASE_DIR, '1-Standard Cost.xlsx')
    classic_pon_file_location = os.path.join(BASE_DIR, '2-Substitution Matrix.xlsx')
    substitution_pon_file_location = os.path.join(BASE_DIR, '2-Substitution Matrix.xlsx')
    shared_depot_file_location = os.path.join(BASE_DIR, 'shared.csv')
    gross_quantity_bom_depot_file_location = os.path.join(BASE_DIR, 'gross_quantity_bom.csv')
    gross_quantity_mtbf_bom_depot_file_location = os.path.join(BASE_DIR, 'gross_quantity_mtbf_bom.csv')
    gross_depot_file_location = os.path.join(BASE_DIR, 'grossdepot.csv')
    fruc_file_location = os.path.join(BASE_DIR, 'fruc.csv')
    Bestal_file_location = os.path.join(BASE_DIR, 'Timbuktu - Clean.csv')
    end_customer_file_location = os.path.join(BASE_DIR, '4-SPMS_Reference_Data.xlsx')
    final_output = os.path.join(BASE_DIR, 'output.csv')
    shared_depot_file = os.path.join(BASE_DIR, 'shared_depot.csv')

    all_parts_array = [
        {"fname": standard_cost_file_location, "sheet": "STD COST ",
         "part_name_column": "Material Desciption = Part Name"},
        {"fname": classic_pon_file_location, "sheet": "Substitution Matrix",
         "part_name_column": "ClassicPON"},
        {"fname": substitution_pon_file_location, "sheet": "Substitution Matrix",
         "part_name_column": "SubstitutionPON"},
        {"fname": spms_reference_file_location, "sheet": "Misnomer PONs",
         "part_name_column": "Correct PON"},
        {"fname": spms_reference_file_location, "sheet": "Unspared PONs",
         "part_name_column": "Unspared PONs"}

    ]

    find_part_family_array = [
        {"fname": spms_reference_file_location, "sheet": "Rel Class To Pon",
         "part_name_column": "Item Number", "parts_family": "REL CLASS"}
    ]

    find_material_number_array = [
        {"fname": standard_cost_file_location, "sheet": "STD COST ",
         "part_name_column": "Material Desciption = Part Name",
         "material_number_column": "Material Number"},
        {"fname": sap_export_file_location, "sheet": "Sheet1",
         "part_name_column": "Material Description = Part Name",
         "material_number_column": "Material Number"}
    ]

    find_spared_attribute = [
        {"fname": spms_reference_file_location, "sheet": "Unspared PONs",
         "part_name_column": "Unspared PONs"}
    ]

    find_end_customer_array = [
        {"fname": end_customer_file_location, "sheet": "Node to Depot",
         "keep_column": ['Customer', 'Node Name']}
    ]

    find_high_parts = [
        {"fname": substitution_pon_file_location, "sheet": "Substitution Matrix",
         "keep_column": ['ClassicPON', 'SubstitutionPON']}
    ]

    part_cost = [
        {"fname": standard_cost_file_location, "sheet": "STD COST "
         }
    ]

    find_misnomer_pon = [
        {"fname": spms_reference_file_location, "sheet": "Misnomer PONs"}

    ]

    site_node = [
        {"fname": spms_reference_file_location, "sheet": "Node to Depot"}

    ]
