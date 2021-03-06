from datetime import datetime
from app import app
from app import csvs, excel, mytext
from app.tasks import celery, part_table_creation, depot_table_creation, node_table_creation, \
    high_spare_table_creation, misnomer_table_creation, ratio_table_creation
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
    ''' It populates 2 tables parts & std_cost '''

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
        raise FileFormatIssue(depot_file, "More than required 12 columns, BAD Depot File")

    depot_cols = ['depot_name', 'depot_address', 'city', 'state', 'country', 'region', 'hub',
                  'partner', 'partner_warehouse_code', 'contact', 'lat', 'long']

    if set(depot_df.columns.values.tolist()) != set(depot_cols):
        raise FileFormatIssue(depot_file, "Header mismatch, BAD Depot File")


class UploadDepot(Resource):
    ''' It populates depot table '''
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


def check_node_file(node_file, extension):

    if extension.lower() == '.csv':
        node_df = pd.read_csv(node_file, nrows=200)

    elif extension.lower() == '.txt':
        node_df = pd.read_csv(node_file, sep='\t', nrows=200)

    elif extension.lower() == '.xls' or extension.lower() == '.xlsx':
        node_df = pd.read_excel(node_file)

    node_row, node_cols = node_df.shape
    if node_row < 1:
        raise FileFormatIssue(node_file, "No Records to process, BAD Node File")

    if node_cols < 3:
        raise FileFormatIssue(node_file, "Less than required 3 columns, BAD Node File")

    if node_cols > 3:
        raise FileFormatIssue(node_file, "More than required 3 columns, BAD Node File")

    depot_cols = ['node_name', 'end_customer_node_belongs', 'node_depot_belongs']

    if set(node_df.columns.values.tolist()) != set(depot_cols):
        raise FileFormatIssue(node_file, "Header mismatch, BAD Node File")


class UploadNode(Resource):
    ''' It populates 2 tables node & end_customer '''

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_email_id', type=str, required=True, help='Email ID missing', location='form')
        super(UploadNode, self).__init__()

    def post(self):

        args = self.reqparse.parse_args()
        dest_folder = request.form.get('user_email_id')
        upload_date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        node_file = ''

        for file in request.files.getlist('node_file'):

            name, extension = os.path.splitext(file.filename)

            if extension.lower() == '.csv':
                dir_path = os.path.join(app.config.get("UPLOADED_CSV_DEST"), dest_folder)
                full_path = os.path.abspath(dir_path)
                file.filename = "node_file_{0}{1}".format(upload_date, extension.lower())
                node_file = file.filename
                csvs.save(file, folder=dest_folder)

            node_file = os.path.join(full_path, node_file)
        try:
            check_node_file(node_file, extension)

            #node_table_creation(node_file, extension)
            celery.send_task('app.tasks.node_table_creation', [node_file, extension])
            return jsonify(msg="Node File Uploaded Successfully", http_status_code=200)

        except FileFormatIssue as e:
            return jsonify(msg=e.msg, http_status_code=400)

        except Exception as e:
            print(str(e))
            return jsonify(msg="Error in File Uploading,Please try again", http_status_code=400)


def check_high_spare_file(high_spare_file, extension):

    if extension.lower() == '.csv':
        high_spare_df = pd.read_csv(high_spare_file, nrows=200)

    elif extension.lower() == '.txt':
        high_spare_df = pd.read_csv(high_spare_file, sep='\t', nrows=200)

    elif extension.lower() == '.xls' or extension.lower() == '.xlsx':
        high_spare_df = pd.read_excel(high_spare_file)

    high_spare_row, high_spare_cols = high_spare_df.shape
    if high_spare_row < 1:
        raise FileFormatIssue(high_spare_file, "No Records to process, BAD High Spare File")

    if high_spare_cols < 2:
        raise FileFormatIssue(high_spare_file, "Less than required 2 columns, BAD High Spare File")

    if high_spare_cols > 2:
        raise FileFormatIssue(high_spare_file, "More than required 2 columns, BAD High Spare File")

    high_spare_cols = ['ClassicPON', 'SubstitutionPON']

    if set(high_spare_df.columns.values.tolist()) != set(high_spare_cols):
        raise FileFormatIssue(high_spare_file, "Header mismatch, BAD High Spare File")


class UploadHighSpare(Resource):
    ''' It populates 1 tables high_spare '''

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_email_id', type=str, required=True, help='Email ID missing', location='form')
        super(UploadHighSpare, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        dest_folder = request.form.get('user_email_id')
        upload_date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        high_spare_file = ''

        for file in request.files.getlist('high_spare_file'):

            name, extension = os.path.splitext(file.filename)

            if extension.lower() == '.csv':
                dir_path = os.path.join(app.config.get("UPLOADED_CSV_DEST"), dest_folder)
                full_path = os.path.abspath(dir_path)
                file.filename = "high_spare_file_{0}{1}".format(upload_date, extension.lower())
                high_spare_file = file.filename
                csvs.save(file, folder=dest_folder)

            high_spare_file = os.path.join(full_path, high_spare_file)
        try:
            check_high_spare_file(high_spare_file, extension)

            high_spare_table_creation(high_spare_file, extension)
            celery.send_task('app.tasks.high_spare_table_creation', [high_spare_file, extension])
            return jsonify(msg="High_Spare File Uploaded Successfully", http_status_code=200)

        except FileFormatIssue as e:
            return jsonify(msg=e.msg, http_status_code=400)

        except Exception as e:
            print(str(e))
            return jsonify(msg="Error in File Uploading,Please try again", http_status_code=400)


def check_misnomer_file(misnomer_file, extension):

    if extension.lower() == '.csv':
        misnomer_df = pd.read_csv(misnomer_file, nrows=200)

    elif extension.lower() == '.txt':
        misnomer_df = pd.read_csv(misnomer_file, sep='\t', nrows=200)

    elif extension.lower() == '.xls' or extension.lower() == '.xlsx':
        misnomer_df = pd.read_excel(misnomer_file)

    misnomer_df_row, misnomer_df_cols = misnomer_df.shape
    if misnomer_df_row < 1:
        raise FileFormatIssue(misnomer_file, "No Records to process, BAD Misnomer File")

    if misnomer_df_cols < 2:
        raise FileFormatIssue(misnomer_file, "Less than required 2 columns, BAD Misnomer File")

    if misnomer_df_cols > 2:
        raise FileFormatIssue(misnomer_file, "More than required 2 columns, BAD Misnomer File")

    misnomer_cols = ['Misnomer PON', 'Correct PON']

    if set(misnomer_df.columns.values.tolist()) != set(misnomer_cols):
        raise FileFormatIssue(misnomer_file, "Header mismatch, BAD Misnomer File")


class UploadMisnomer(Resource):
    ''' It populates 1 table misnomer  '''

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_email_id', type=str, required=True, help='Email ID missing', location='form')
        super(UploadMisnomer, self).__init__()

    def post(self):

        args = self.reqparse.parse_args()
        dest_folder = request.form.get('user_email_id')
        upload_date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        misnomer_file = ''

        for file in request.files.getlist('misnomer_file'):

            name, extension = os.path.splitext(file.filename)

            if extension.lower() == '.csv':
                dir_path = os.path.join(app.config.get("UPLOADED_CSV_DEST"), dest_folder)
                full_path = os.path.abspath(dir_path)
                file.filename = "high_spare_file_{0}{1}".format(upload_date, extension.lower())
                misnomer_file = file.filename
                csvs.save(file, folder=dest_folder)

            misnomer_file = os.path.join(full_path, misnomer_file)
        try:
            check_misnomer_file(misnomer_file, extension)

            #misnomer_table_creation(misnomer_file, extension)
            celery.send_task('app.tasks.misnomer_table_creation', [misnomer_file, extension])
            return jsonify(msg="Misnomer File Uploaded Successfully", http_status_code=200)

        except FileFormatIssue as e:
            return jsonify(msg=e.msg, http_status_code=400)

        except Exception as e:
            print(str(e))
            return jsonify(msg="Error in File Uploading,Please try again", http_status_code=400)


def check_ratio_file(ratio_file, extension):
    import numpy as np

    if extension.lower() == '.csv':
        ratio_df = pd.read_csv(ratio_file, nrows=200)

    elif extension.lower() == '.txt':
        ratio_df = pd.read_csv(ratio_file, sep='\t', nrows=200)

    elif extension.lower() == '.xls' or extension.lower() == '.xlsx':
        ratio_df = pd.read_excel(ratio_file)

    # Reformat file to be in proper dataframe

    ratio_df.columns = ratio_df.iloc[np.where((ratio_df.isin(['Products'])) == True)[0]].values[0]
    ratio_df = ratio_df.iloc[(int(np.where((ratio_df.isin(['Products']) == True))[0])) + 1:]

    ratio_df_row, ratio_df_cols = ratio_df.shape
    if ratio_df_row < 1:
        raise FileFormatIssue(ratio_file, "No Records to process, BAD Ratio File")

    if ratio_df_cols < 12:
        raise FileFormatIssue(ratio_file, "Less than required 12 columns, BAD Ratio File")

    if ratio_df_cols > 12:
        raise FileFormatIssue(ratio_file, "More than required 12 columns, BAD Ratio File")

    ratio_cols = ['Products', 'Telcorida MTBF (hrs.)', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    if set(ratio_df.columns.values.tolist()) != set(ratio_cols):
        raise FileFormatIssue(ratio_file, "Header mismatch, BAD Ratio File")


class UploadRatio(Resource):
    ''' It populates 1 table ratio  '''

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_email_id', type=str, required=True, help='Email ID missing', location='form')
        self.reqparse.add_argument('analysis_type', required=True, location='form')
        super(UploadRatio, self).__init__()

    def post(self):

        args = self.reqparse.parse_args()
        dest_folder = request.form.get('user_email_id')
        upload_date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        ratio_file = ''
        analysis_type = request.form.get('analysis_type')

        for file in request.files.getlist('ratio_file'):

            name, extension = os.path.splitext(file.filename)

            if extension.lower() == '.csv':
                dir_path = os.path.join(app.config.get("UPLOADED_CSV_DEST"), dest_folder)
                full_path = os.path.abspath(dir_path)
                file.filename = "high_spare_file_{0}{1}".format(upload_date, extension.lower())
                ratio_file = file.filename
                csvs.save(file, folder=dest_folder)

            ratio_file = os.path.join(full_path, ratio_file)
        try:
            check_ratio_file(ratio_file, extension)

            #ratio_table_creation(ratio_file, extension, analysis_type)
            celery.send_task('app.tasks.ratio_table_creation', [ratio_file, extension, analysis_type])
            return jsonify(msg="Ratio File Uploaded Successfully", http_status_code=200)

        except FileFormatIssue as e:
            return jsonify(msg=e.msg, http_status_code=400)

        except Exception as e:
            print(str(e))
            return jsonify(msg="Error in File Uploading,Please try again", http_status_code=400)

