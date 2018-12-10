import pandas as pd
import sys
import os
from sqlalchemy import create_engine
from app import app
from app import Configuration
from app.tasks.common_functions import clean_pon_names, to_sql_customer_dna_record

engine = create_engine(Configuration.ECLIPSE_DATA_DB_URI)



def cleaned_dna_file(dna_file):

    # Read the input dna file

    input_db = pd.read_csv(dna_file, sep=',')

    # Perform any basic clean up activities -  Clean the PON, and installed equipment,
    # strip any special characters. Other than ‘.’ and ‘-’ ,’\’

    input_db = clean_pon_names(input_db)
    return input_db





