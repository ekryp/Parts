import os
import shutil

import pandas as pd
from app.auth.authorization import requires_auth
from flask import jsonify
from flask import request
from flask_restful import Resource, reqparse

from app import app
from app import csvs
from app.tasks import celery
from app.utils.utils import get_ekryp_partner_id_from_token




def check_file_size(num):
    """
    this function checks 100MB file size
    """
    if num <=104857600:
        return False
    else:
        return True

class FileSizeException(Exception):
    def __init__(self, filename, msg):
        self.filename = filename
        self.msg = msg

class FileFormatIssue(Exception):
    def __init__(self, filename, msg):
        self.filename = filename
        self.msg = msg

def incident_file_check(file,owd,full_path):
    columns = ["Serial Number","Service Request Date" ,"Service Request Time","Service Ticket Number","Service Rep",
               "Priority","Incident Category","Initial Reason","Final Reason","Status"]
    try:
        df = pd.read_csv(file,index_col=False)
    except IndexError:
        os.chdir(owd)
        shutil.rmtree(full_path)
        raise FileFormatIssue(file, "Number of columns are greater than number of headers")
    if len(df.columns) < 10:
        os.chdir(owd)
        shutil.rmtree(full_path)
        raise FileFormatIssue(file,"Number of columns are less than minimum columns 10")
    if (df.columns.values[:10] == columns).all() == True:
        return True
    else:
        os.chdir(owd)
        shutil.rmtree(full_path)
        raise FileFormatIssue(file, "Column Header names mismatch")

def installed_base_file_check(file,owd,full_path):

    columns = ["Serial Number", "Site ID", "Firmware ID", "Asset Attribute  Identifier", "Product Desc"
        , "Active Status", "Warranty End Date", "Service End Date", "Service Start Date", "Installed Date",
        "Latest Inactive Date", "Service Provider Id", "Model_ID", "Model Name", "Model Group ID",
        "Model Group Name", "Category", "Category Name", "Type Id", "type_name"]
    try:
        df = pd.read_csv(file,index_col=False)
    except IndexError:
        os.chdir(owd)
        shutil.rmtree(full_path)
        raise FileFormatIssue(file, "Number of columns are greater than number of headers")
    if len(df.columns) < 20:
        os.chdir(owd)
        shutil.rmtree(full_path)
        raise FileFormatIssue(file,"Number of columns are less than minimum columns 21")
    if (df.columns.values[:20] == columns).all() == True:
        return True
    else:
        os.chdir(owd)
        shutil.rmtree(full_path)
        raise FileFormatIssue(file, "Column Header names mismatch")


def asset_life_event_file_check(file,owd,full_path):
    columns = ["Serial Number","Life Event Code","Event date","Life Event Value"]
    try:
        df = pd.read_csv(file,index_col=False)
    except IndexError:
        raise FileFormatIssue(file, "Number of columns are greater than number of headers")
    if len(df.columns) < 4:
        os.chdir(owd)
        shutil.rmtree(full_path)
        raise FileFormatIssue(file,"Number of columns are less than minimum columns 4")
    if (df.columns.values[:4] == columns).all() == True:
        return True
    else:
        os.chdir(owd)
        shutil.rmtree(full_path)
        raise FileFormatIssue(file, "Column Header names mismatch")

def asset_conditions_events_check(file,owd,full_path):
    columns = ["Serial Number","Date","Time","Code Id","Code","Code Type","Code Description","Code Detail"
        ,"Code area","Code Criticality","Key Value Pairs"]
    try:
        df = pd.read_csv(file,index_col=False)
    except IndexError:
        raise FileFormatIssue(file, "Number of columns are greater than number of headers")
    if len(df.columns) < 11:
        os.chdir(owd)
        shutil.rmtree(full_path)
        raise FileFormatIssue(file,"Number of columns are less than minimum columns 11")
    if (df.columns.values[:11] == columns).all() == True:
        return True
    else:
        os.chdir(owd)
        shutil.rmtree(full_path)
        raise FileFormatIssue(file, "Column Header names mismatch")

def daily_work_file_check(file,owd,full_path):
    columns = ["Serial Number","Date","Time","WORK_TYPE","WORK_UNITS"]
    try:
        df = pd.read_csv(file,index_col=False)
    except IndexError:
        raise FileFormatIssue(file, "Number of columns are greater than number of headers")
    if len(df.columns) < 5:
        os.chdir(owd)
        shutil.rmtree(full_path)
        raise FileFormatIssue(file,"Number of columns are less than minimum columns 5")
    if (df.columns.values[:5] == columns).all() == True:
        return True
    else:
        os.chdir(owd)
        shutil.rmtree(full_path)
        raise FileFormatIssue(file, "Column Header names mismatch")


def Basic_validation(dest_folder):
    dir_path = os.path.join(app.config.get("UPLOADED_CSV_DEST"),dest_folder)
    full_path= os.path.abspath(dir_path)
    owd = os.getcwd()
    os.chdir(full_path)
    file_validation_function_call = {
        "incident_{0}.{1}".format(dest_folder, 'csv'): incident_file_check,
        "installed_base_{0}.{1}".format(dest_folder, 'csv'): installed_base_file_check,
        "asset_life_event_{0}.{1}".format(dest_folder, 'csv'): asset_life_event_file_check,
        "asset_conditions_events_{0}.{1}".format(dest_folder, 'csv'): asset_conditions_events_check,
        "daily_work_{0}.{1}".format(dest_folder, 'csv'): daily_work_file_check
    }
    try:
        for files in  os.listdir(full_path):
            file_info = os.stat(files)
            is_greater = check_file_size(file_info.st_size)
            if is_greater:
                os.chdir(owd)
                shutil.rmtree(full_path)
                raise FileSizeException(os.path.basename(files),"File Size should be less than 100MB")
            try:
                is_invalid = file_validation_function_call.get(files)(files,owd,full_path)
            except TypeError:
                pass

    finally:
            os.chdir(owd)

class UploadCSV(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email_id', type=str, required=True, help='Email ID missing', location='args')
        super(UploadCSV, self).__init__()

    @requires_auth
    def post(self):
        args = self.parser.parse_args()
        email_id = args['email_id']
        auth = request.headers.get("Authorization", None)
        ekryp_partner_id = get_ekryp_partner_id_from_token(auth)
        dest_folder= str(ekryp_partner_id)
        dir_path = os.path.join(app.config.get("UPLOADED_CSV_DEST"), dest_folder)
        full_path = os.path.abspath(dir_path)
        try:
            shutil.rmtree(full_path)
        except FileNotFoundError:
            pass
        error_file_mapping = {
            "incident_{0}.{1}".format(ekryp_partner_id, 'csv'): 'incident_key',
            "installed_base_{0}.{1}".format(ekryp_partner_id, 'csv'): 'installed_base_key',
            "asset_life_event_{0}.{1}".format(ekryp_partner_id, 'csv'): 'asset_life_event_key',
            "asset_conditions_events_{0}.{1}".format(ekryp_partner_id, 'csv'): 'asset_conditions_events_key',
            "daily_work_{0}.{1}".format(ekryp_partner_id, 'csv'): 'daily_work_key'
        }
        try:
            for file in request.files.getlist('installed_base_key'):
                file.filename = "installed_base_{0}.{1}".format(ekryp_partner_id,'csv')
                csvs.save(file, folder=dest_folder)

            for file in request.files.getlist('incident_key'):
                file.filename = "incident_{0}.{1}".format(ekryp_partner_id,'csv')
                csvs.save(file,folder=dest_folder)

            for file in request.files.getlist('asset_life_event_key'):
                file.filename = "asset_life_event_{0}.{1}".format(ekryp_partner_id,'csv')
                csvs.save(file, folder=dest_folder)

            for file in request.files.getlist('asset_conditions_events_key'):
                file.filename = "asset_conditions_events_{0}.{1}".format(ekryp_partner_id,'csv')
                csvs.save(file, folder=dest_folder)

            for file in request.files.getlist('daily_work_key'):
                file.filename = "daily_work_{0}.{1}".format(ekryp_partner_id,'csv')
                csvs.save(file, folder=dest_folder)
            try:
                Basic_validation(dest_folder)


            except FileSizeException as e:
                return jsonify(msg=e.msg,key=error_file_mapping.get(e.filename), http_status_code=400)
            except FileFormatIssue as e:
                return jsonify(msg=e.msg, key=error_file_mapping.get(e.filename),
                               http_status_code=400)


            add_prospect(ekryp_partner_id, email_id)
            update_prospect_step(1, int(dest_folder))
            celery.send_task('app.tasks.task_customer_creation_mysql_ingestion',[ekryp_partner_id,email_id])
            # task_customer_creation_mysql_ingestion(ekryp_partner_id,email_id)
            celery.send_task('app.tasks.task_data_creation_mysql_ingestion',[ekryp_partner_id])
            # task_data_creation_mysql_ingestion(ekryp_partner_id)
            celery.send_task('app.tasks.task_json_creation_per_file', [ekryp_partner_id,email_id])
            #task_json_creation_per_file(ekryp_partner_id,email_id)
            celery.send_task('app.tasks.task_tsv_creation_per_file', [ekryp_partner_id, email_id])
            #task_tsv_creation_per_file(ekryp_partner_id,email_id)
            celery.send_task('app.tasks.task_druid_ingestion_per_file', [ekryp_partner_id, email_id])
            #task_druid_ingestion_per_file(ekryp_partner_id,email_id)
            celery.send_task('app.tasks.folder_structure_creation', [ekryp_partner_id])
            #folder_structure_creation(ekryp_partner_id)
            return jsonify(msg="Files Uploaded Successfully", http_status_code=200)
        except:
            return jsonify(msg="Error in File Uploading,Please try again",http_status_code=400)

    def options(self):
        pass