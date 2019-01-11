from datetime import datetime
from app import app
from app import csvs, excel, mytext
from app.tasks import celery, part_table_creation, depot_table_creation
from flask import jsonify
from flask import request
from flask_restful import Resource
from flask_restful import reqparse
import pandas as pd
import pdb
import os
from app.resources.infinera import FileFormatIssue


def check_part_file(part_file, extension):

    if extension.lower() == '.csv':
        part_df = pd.read_csv(part_file, nrows=200)

    elif extension.lower() == '.txt':
        part_df = pd.read_csv(part_file, sep='\t', nrows=200)

    elif extension.lower() == '.xls' or extension.lower() == '.xlsx':
        part_df = pd.read_excel(part_file)

    part_row, part_cols = part_df.shape
    if part_row < 1:
        raise FileFormatIssue(part_file, "No Records to process, BAD Part File")

    if part_cols < 5:
        raise FileFormatIssue(part_file, "Less than required 5 columns, BAD Part File")

    if part_cols > 5:
        raise FileFormatIssue(part_file, "More than required 5 columns, BAD Part File")

    part_cols = ['material_number', 'part_name', 'part_reliability_class', 'spared_attribute', 'standard_cost']

    if set(part_df.columns.values.tolist()) != set(part_cols):
        raise FileFormatIssue(part_file, "Header mismatch, BAD Part File")


class UploadParts(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_email_id', type=str, required=True, help='Email ID missing', location='form')
        super(UploadParts, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        dest_folder = request.form.get('user_email_id')
        upload_date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        parts_file = ''

        for file in request.files.getlist('parts_file'):

            name, extension = os.path.splitext(file.filename)

            if extension.lower() == '.csv':
                dir_path = os.path.join(app.config.get("UPLOADED_CSV_DEST"), dest_folder)
                full_path = os.path.abspath(dir_path)
                file.filename = "parts_file_{0}{1}".format(upload_date, extension.lower())
                parts_file = file.filename
                csvs.save(file, folder=dest_folder)

            parts_file = os.path.join(full_path, parts_file)
        try:
            check_part_file(parts_file, extension)

            #part_table_creation(parts_file, extension)
            celery.send_task('app.tasks.part_table_creation', [parts_file, extension])
            return jsonify(msg="Part File Uploaded Successfully", http_status_code=200)

        except FileFormatIssue as e:
            return jsonify(msg=e.msg, http_status_code=400)

        except Exception as e:
            print(str(e))
            return jsonify(msg="Error in File Uploading,Please try again", http_status_code=400)


def check_depot_file(depot_file, extension):

    if extension.lower() == '.csv':
        depot_df = pd.read_csv(depot_file, nrows=200)

    elif extension.lower() == '.txt':
        depot_df = pd.read_csv(depot_file, sep='\t', nrows=200)

    elif extension.lower() == '.xls' or extension.lower() == '.xlsx':
        depot_df = pd.read_excel(depot_file)

    depot_row, depot_cols = depot_df.shape
    if depot_row < 1:
        raise FileFormatIssue(depot_file, "No Records to process, BAD Depot File")

    if depot_cols < 12:
        raise FileFormatIssue(depot_file, "Less than required 12 columns, BAD Depot File")

    if depot_cols > 12:
        raise FileFormatIssue(depot_file, "More than required 5 columns, BAD Depot File")

    depot_cols = ['depot_name', 'depot_address', 'city', 'state', 'country', 'region', 'hub',
                  'partner', 'partner_warehouse_code', 'contact', 'lat', 'long']

    if set(depot_df.columns.values.tolist()) != set(depot_cols):
        raise FileFormatIssue(depot_file, "Header mismatch, BAD Depot File")


class UploadDepot(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_email_id', type=str, required=True, help='Email ID missing', location='form')
        super(UploadDepot, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        dest_folder = request.form.get('user_email_id')
        upload_date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        depot_file = ''

        for file in request.files.getlist('depot_file'):

            name, extension = os.path.splitext(file.filename)

            if extension.lower() == '.csv':
                dir_path = os.path.join(app.config.get("UPLOADED_CSV_DEST"), dest_folder)
                full_path = os.path.abspath(dir_path)
                file.filename = "depot_file_{0}{1}".format(upload_date, extension.lower())
                depot_file = file.filename
                csvs.save(file, folder=dest_folder)

            depot_file = os.path.join(full_path, depot_file)
        try:
            check_depot_file(depot_file, extension)

            #depot_table_creation(depot_file, extension)
            celery.send_task('app.tasks.depot_table_creation', [depot_file, extension])
            return jsonify(msg="Depot File Uploaded Successfully", http_status_code=200)

        except FileFormatIssue as e:
            return jsonify(msg=e.msg, http_status_code=400)

        except Exception as e:
            print(str(e))
            return jsonify(msg="Error in File Uploading,Please try again", http_status_code=400)




