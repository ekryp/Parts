from app.configs.base_config import BaseConfig
import os


class Configuration(BaseConfig):
    DEBUG = True

    EKRYP_DATA_DB_URI = "mysql+cymysql://ashish:Ekryp#1234@35.199.174.191/ekryp_core_prospect"

    EKRYP_USER_DB_URI = "mysql+cymysql://ashish:Ekryp#1234@35.199.174.191/ekryp_prospect"

    PROSPECT_DB_URL = "mysql+cymysql://ashish:Ekryp#1234@35.199.174.191/ekryp_prospect_db"
	
    AIRFLOW_DB_URL = "mysql+cymysql://ashish:Ekryp#1234@35.199.174.191/ekryp_challenge"

    INFINERA_DB_URL = "mysql+cymysql://ashish:Ekryp#1234@35.199.174.191/infinera"

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

    ECLIPSE_DATA_DB_URI = "mysql+cymysql://ashish:Ekryp#1234@35.199.174.191/infinera"
    BASE_DIR = r'/Users/anup/eKryp/Parts/backend/static'

    sap_export_file_location = os.path.join(BASE_DIR, '3-SAPexport.XLSX')
    sap_export = os.path.join(BASE_DIR, '3-SAPexport.XLSX')
    spms_reference_file_location = os.path.join(BASE_DIR, '4-SPMS_Reference_Data.xlsx')
    standard_cost_file_location = os.path.join(BASE_DIR, '1-Standard Cost.xlsx')
    classic_pon_file_location = os.path.join(BASE_DIR, '2-Substitution Matrix.xlsx')
    substitution_pon_file_location = os.path.join(BASE_DIR, '2-Substitution Matrix.xlsx')
    #shared_depot_file_location = os.path.join(BASE_DIR, 'shared.csv')
    gross_depot_file_location = os.path.join(BASE_DIR, 'grossdepot.csv')
    fruc_file_location = 'fruc.csv'
    bom_table = 'bom_table.csv'
    mtbf_bom_table = 'mtbf_bom_table.csv'
    DNA_BOM = 'DNA_BOM.csv'
    MTBF_BOM = 'MTBF_BOM.csv'
    summary_output = 'summary_output.csv'
    shared_depot_file_location = "shared_depot_file_location.csv"
    gross_quantity_bom_depot_file_location = "gross_quantity_bom_depot_file_location.csv"
    gross_quantity_mtbf_bom_depot_file_location = 'gross_quantity_mtbf_bom_depot_file_location.csv'
    net_depot = "net_depot.csv"
    final_output ="final_output.csv"
    Bestal_file_location = os.path.join(BASE_DIR, 'Bestel_EqptMngr_FlatFile_1.txt')
    end_customer_file_location = os.path.join(BASE_DIR, '4-SPMS_Reference_Data.xlsx')

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

