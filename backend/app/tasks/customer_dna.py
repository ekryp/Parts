import pandas as pd
import sys
import os
from sqlalchemy import create_engine
from app import app
from app import Configuration
from app.tasks.common_functions import clean_pon_names, to_sql_customer_dna_record

engine = create_engine(Configuration.ECLIPSE_DATA_DB_URI)


def check_file_validity(file):
    name, extension = os.path.splitext(file)

    if extension.lower() == '.txt':
        data = pd.read_csv(file, sep = '\t', keep_default_na=False, na_values=[""])
    elif extension.lower() == '.csv':
        data = pd.read_csv(file,  keep_default_na=False, na_values=[""])
    elif extension.lower() == '.xls' or extension.lower() == '.xlsx':
        data = pd.read_excel(file,  keep_default_na=False, na_values=[""])
    else:
        print('unsupported type')
        exit()
    return data


def clean_file(file):
    data_frame_list = []
    data_frame = pd.DataFrame()
    #step 1
    data = check_file_validity(file)

    #step 3
    valid_columns = ['#Type', 'Node ID', 'Node Name', 'AID', 'InstalledEqpt', 'Product Ordering Name', 'Part#', 'Serial#']

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

        return data_frame_file

    else:

        new_data = data[valid_columns]
        new_data['Source'] = os.path.basename(file)
        return new_data



def cleaned_dna_file(dna_file):

    # Read the input dna file

    input_db = clean_file(dna_file)
    # Perform any basic clean up activities -  Clean the PON, and installed equipment,
    # strip any special characters. Other than ‘.’ and ‘-’ ,’\’

    input_db = clean_pon_names(input_db)
    return input_db





