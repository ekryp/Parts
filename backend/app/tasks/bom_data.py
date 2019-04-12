import pandas as pd
import os


def check_file_validity(file):
    name, extension = os.path.splitext(file)

    if extension.lower() == '.txt':
        data = pd.read_csv(file, sep='\t')
    elif extension.lower() == '.csv':
        data = pd.read_csv(file)
    elif extension.lower() == '.xls' or extension.lower() == '.xlsx':
        data = pd.read_excel(file)

    data.rename(columns={
        'Depot': 'Node Depot Belongs',
        'Part': 'Product Ordering Name',
        'Quantity': 'PON Quantity'
    }, inplace=True)
    return data

def read_bom_file(bom_file):
    # Read the input bom file
    input_db = check_file_validity(bom_file)
    return input_db