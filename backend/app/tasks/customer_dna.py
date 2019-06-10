import pandas as pd
import sys
import os
from sqlalchemy import create_engine

from app import app
from app import Configuration
from app.tasks.common_functions import clean_pon_names, to_sql_customer_dna_record

engine = create_engine(Configuration.ECLIPSE_DATA_DB_URI, connect_args=Configuration.ssl_args)


def check_file_validity(file, is_inservice_only):

    name, extension = os.path.splitext(file)

    if extension.lower() == '.txt':
        data = pd.read_csv(file, sep = '\t', keep_default_na=False, na_values=[""])
    elif extension.lower() == '.csv':
        data = pd.read_csv(file,  keep_default_na=False, na_values=[""])
    elif extension.lower() == '.xls' or extension.lower() == '.xlsx':
        data = pd.read_excel(file,  keep_default_na=False, na_values=[""])
    elif extension.lower() == '.tsv':
        lookup = '#Type'
        lines = []
        with open(file) as myFile:
            for num, line in enumerate(myFile, 1):
                if lookup in line:
                    lines.append(num)

        data_frame_list = []
        data = pd.DataFrame()
        print(lines)
        if is_inservice_only:
            columns = ['#Type', 'Node ID', 'Node Name', 'AID', 'InstalledEqpt', 'Product Ordering Name',
                   'Part#', 'Serial#', 'Service State']
        else:
            columns = ['#Type', 'Node ID', 'Node Name', 'AID', 'InstalledEqpt', 'Product Ordering Name',
                   'Part#', 'Serial#']
        for index, line in enumerate(lines):
            data_frame = pd.DataFrame()
            try:
                print("getting data from {0} to {1}".format(lines[index] - 1, lines[index+1] - lines[index] - 2))
                data_frame = pd.read_csv(file, sep='\t', skiprows=lines[index] - 1, nrows=lines[index+1] - lines[index] - 2, usecols=columns)

            except:
                print("getting data from {0} to end ".format(lines[index] - 1))
                data_frame = pd.read_csv(file, sep='\t', skiprows=lines[index] - 1, usecols=columns)

            data_frame_list.append(data_frame)

        data = pd.concat(data_frame_list)
    else:
        print('unsupported type')
        exit()
    return data


def clean_file(file, is_inservice_only):

    data_frame_list = []
    data_frame = pd.DataFrame()
    #step 1
    data = check_file_validity(file, is_inservice_only)

    #step 3
    if is_inservice_only:
        valid_columns = ['#Type', 'Node ID', 'Node Name', 'AID', 'InstalledEqpt', 'Product Ordering Name',
                         'Part#', 'Serial#', 'Service State']
    else:
        valid_columns = ['#Type', 'Node ID', 'Node Name', 'AID', 'InstalledEqpt', 'Product Ordering Name',
                         'Part#', 'Serial#']

    index = data[(data.values == '#Type')].index

    #step 3.
    if index.empty == False:

        for col in range(len(index)):
            #step 4
            try:
                end_index = data.index[data.iloc[:, 0].isnull().values][col + 1]
            except:
                #Because we want last row + 1
                end_index = (data.index[-1] + 1)
            #step 4.
            data_frame = data[index[col]: end_index]

            #set row with #Type as first row as column
            data_frame.columns = data.iloc[index[col]]
            #select only valid columns
            data_frame = data_frame[valid_columns]

            #step 6
            data_frame = data_frame[~(data_frame['#Type'].str.contains('#Type', na=False))]
            data_frame_list.append(data_frame)
        data_frame_file = pd.concat(data_frame_list)

        #step 7
        data_frame_file['Source'] = os.path.basename(file)

        if is_inservice_only:
            # Keep only in_service pon
            mask = data_frame_file['Service State'] == 'In-Service'
            print(data_frame_file.shape)
            data_frame_file = data_frame_file[mask]
            data_frame_file = data_frame_file.drop(['Service State'], 1)
            print(data_frame_file.shape)
            return data_frame_file

        else:
            return data_frame_file

    else:

        new_data = data[valid_columns]
        new_data['Source'] = os.path.basename(file)
        if is_inservice_only:
            # Keep only in_service pon
            mask = new_data['Service State'] == 'In-Service'
            print(new_data.shape)
            new_data = new_data[mask]
            new_data = new_data.drop(['Service State'], 1)
            print(new_data.shape)
            return new_data
        else:
            return new_data


def cleaned_dna_file(dna_file, is_inservice_only):

    # Read the input dna file

    input_db = clean_file(dna_file, is_inservice_only)

    # Perform any basic clean up activities -  Clean the PON, and installed equipment,
    # strip any special characters. Other than ‘.’ and ‘-’ ,’\’

    input_db = clean_pon_names(input_db)
    return input_db




