import math
import json
import numpy as np
import pandas as pd
from app import Configuration
from app import app
from app.tasks.common_functions import fetch_db, misnomer_conversion, \
    check_in_std_cst, validate_pon, validate_depot, process_error_pon, \
    to_sql_customer_dna_record, read_sap_export_file, to_sql_current_inventory, \
    add_hnad, to_sql_bom, read_data, to_sql_mtbf, to_sql_current_ib, to_sql_part_table,\
    to_sql_std_cost_table, to_sql_depot_table, to_sql_node_table, to_sql_end_customer_table, \
    to_sql_high_spare_table, to_sql_misnomer_table, to_sql_reliability_class_table, to_sql_bom_record,\
    validate_pon_for_bom, validate_depot_for_bom, to_sql_end_customer, check_analysis_task_status, to_sql_lab_systems, \
    get_part_names_for_adv_settings

from app.tasks.customer_dna import cleaned_dna_file
from celery import Celery
from sqlalchemy import create_engine
import requests
from flask_restful import Resource
from app.tasks.bom_data import read_bom_file


engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args)
connection = Configuration.INFINERA_DB_URL


class CustomException(Exception):
    def __init__(self, msg):
        self.msg = msg


def make_celery(app):
    celery = Celery(app.import_name,
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


celery = make_celery(app)


def add_prospect(email_id):
    engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args)
    selectquery = "select prospects_id FROM prospect_details where prospects_email='{0}'".format(email_id)
    result = engine.execute(selectquery).fetchone()
    if result is not None:
        return result[0]
    else:
        query = "insert into prospect_details (prospects_email) values('{0}')".format(email_id)
        engine.execute(query)
        result = engine.execute(selectquery).fetchone()
        return result[0]


def update_prospect_step(prospects_id, step_id, analysis_date):
    engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args)
    try:
        selectquery = "select * FROM prospect_status where analysis_request_time='{0}'" \
                      "and prospects_id={1}".format(analysis_date, prospects_id)
        result = engine.execute(selectquery).fetchone()
        if result is None:
            query = "insert into prospect_status (prospects_id,prospects_step,analysis_request_time) values({0},{1},'{2}')".format(prospects_id,
                                                                                                 step_id, analysis_date)
            print(query)
            engine.execute(query)

        else:
            query = "update prospect_status set prospects_step = {0} where prospects_id = {1}" \
                    " and analysis_request_time='{2}'".format(step_id, prospects_id, analysis_date)
            print(query)
            engine.execute(query)

    except:
        print("Failed to update status for prospects_id {0}".format(prospects_id))


def shared_function(dna_file, sap_file, analysis_date, analysis_id, prospect_id, replenish_time, is_inservice_only, item_category, product_category, product_family, product_phase, product_type):

    # 5.4 Load all Data elements from Reference Data
    (misnomer_pons, standard_cost, node, spared_pons, highspares, get_ratio_to_pon, parts,
     parts_cost, high_spares, depot) = fetch_db(replenish_time)

    # clean PONs, part# and installed equipments
    input_db = cleaned_dna_file(dna_file, is_inservice_only)


    # 5.5 Convert Misnomer PON to correct PON
    # PON with no misnomers
    input_with_no_misnomer_pon = misnomer_conversion(input_db, misnomer_pons)
    to_sql_customer_dna_record('customer_dna_record', input_db, analysis_date, analysis_id)

    update_prospect_step(prospect_id, 2, analysis_date)  # Dump customer_dna Table Status

    # 5.6 Apply Standard Cost Rule
    input_with_no_misnomer_pon = check_in_std_cst(input_with_no_misnomer_pon, standard_cost)

    # Assign PON to Installed equipments to remove any ambiguity
    input_with_no_misnomer_pon['InstalledEqpt'] = input_with_no_misnomer_pon['Product Ordering Name']

    # 5.7 Validate PONs and Depot
    valid_pon = validate_pon(input_with_no_misnomer_pon, analysis_date, analysis_id)

    # 5.8 Identify Valid Sparable Items and Identify Error Conditions

    # 5.8.1 Calculate node_to_depot
    valid_pon = pd.merge(valid_pon, node, left_on='Node Name', right_on='node_name', how='left')
    valid_pon = validate_depot(valid_pon, analysis_date, analysis_id)

    # Add node_depot_belongs attribute ,If True PON has depot name
    valid_pon['has_node_depot'] = False  # flag used in finding error 5
    valid_pon.loc[(valid_pon['node_depot_belongs'].notna()), 'has_node_depot'] = True

    # 5.8.2 Collect attributes A) PON Has Std Cost or Not
    valid_pon = pd.merge(valid_pon, standard_cost, left_on=['Product Ordering Name'], right_on=['part_name'],
                         how='left')
    # Remove unnecessary column generated by merge

    valid_pon = valid_pon.drop(['created_at', 'updated_at', 'Source'], 1)
    valid_pon['has_std_cost'] = False  # flag used in finding error 3
    valid_pon.loc[(valid_pon['standard_cost'].notna()), 'has_std_cost'] = True

    # 5.8.2 Collect attributes - B) PON is Sparrable or Not
    valid_pon['is_sparrable'] = False
    valid_pon = pd.merge(valid_pon, spared_pons, left_on=['Product Ordering Name'], right_on=['part_name'], how='inner')

    valid_pon.loc[(valid_pon['Product Ordering Name'] == valid_pon['part_name_x']), 'is_sparrable'] = True

    # Remove unnecessary column generated by merge
    valid_pon = valid_pon.drop(['part_name_x', 'part_name_y'], 1)

    # Keep only sparable pons
    valid_pon = valid_pon[valid_pon['is_sparrable'] == True]

    # Added Code for adv settings here
    # First check whther we received adv setting
    # If received then only get parts with matching adv settings

    if item_category or product_category or product_family or product_phase or product_type:
        part_in_adv_settings = get_part_names_for_adv_settings(item_category, product_category, product_family, product_phase, product_type)
        if part_in_adv_settings.empty:
            raise CustomException("no valid parts in advance settings - Aborting the analysis")
        valid_pon = pd.merge(valid_pon, part_in_adv_settings, how='inner', left_on='Product Ordering Name', right_on='parts_adv')
        valid_pon = valid_pon.drop(['parts_adv'], 1)

    # all_valid conditions
    # PON with sparable, has_std_cost,has_node_depot and valid pon_name & depot name
    all_valid = valid_pon[((valid_pon['has_std_cost'] == True) & (valid_pon['has_node_depot'] == True))]
    if all_valid.empty:
        raise CustomException("no valid record to process - Aborting the analysis")

    invalid_pon = valid_pon[~((valid_pon['has_std_cost'] == True) & (valid_pon['has_node_depot'] == True))]
    # 5.9 Process Error Records - Store Invalid PONS with Proper Reason
    if not invalid_pon.empty:
        process_error_pon('error_records', invalid_pon, analysis_date, analysis_id)

    update_prospect_step(prospect_id, 3, analysis_date)  # Dump error_records Table Status

    # 5.9 Process Error Records - Compare Valid PON against

    sap_inventory = read_sap_export_file(sap_file)

    # keep only valid rows, keep rows having part_names are present in sap_inventory
    unique_parts_in_sap = sap_inventory['Material Description = Part Name'].unique()

    not_in_sap_file = all_valid[~all_valid['Product Ordering Name'].isin(unique_parts_in_sap)]
    if not not_in_sap_file.empty:
        not_in_sap_file['present_in_sap'] = False  # flag used in finding error 1
        process_error_pon('error_records', not_in_sap_file, analysis_date, analysis_id)

    # check if item is high spare & high spare not in SAP file
    all_valid = pd.merge(all_valid, high_spares, left_on=['Product Ordering Name'], right_on=['part_name'], how='left')

    all_valid['has_high_spare'] = False
    all_valid.loc[(all_valid['high_spare'].notna()), 'has_high_spare'] = True
    high_spares_not_in_sap = all_valid[~all_valid['has_high_spare'] == True & all_valid['high_spare'].isin(unique_parts_in_sap)]

    if not high_spares_not_in_sap.empty:
        high_spares_not_in_sap['high_spare_present_in_sap'] = False  # flag used in finding error 2
        process_error_pon('error_records', high_spares_not_in_sap, analysis_date, analysis_id)

    # Remove the rows for item who has high spares & high spares are not present in SAP file ,error condition 2
    all_valid = all_valid[all_valid['has_high_spare'] == True & all_valid['high_spare'].isin(unique_parts_in_sap)]

    # Remove rows which has high spares ,but high spares do not have std_cost
    all_valid = pd.merge(all_valid, standard_cost, left_on='high_spare', right_on='part_name', how='left')
    high_spare_no_std_cost = all_valid[all_valid['has_high_spare'] == True & all_valid['standard_cost_y'].isna()]

    if not high_spare_no_std_cost.empty:
        high_spare_no_std_cost = high_spare_no_std_cost.drop(['material_number_y', 'standard_cost_y', 'part_name_y'], 1)
        high_spare_no_std_cost.rename(columns={
            'standard_cost_x': 'standard_cost',
            'part_name_x': 'part_name',
            'material_number_x': 'material_number',
        }, inplace=True
        )
        high_spare_no_std_cost['high_spare_no_std_cost'] = False  # flag used in finding error 7
        process_error_pon('error_records', high_spare_no_std_cost, analysis_date, analysis_id)

    all_valid = all_valid[all_valid['has_high_spare'] == True & all_valid['standard_cost_y'].notna()]
    all_valid.rename(columns={
        'standard_cost_x': 'standard_cost',
        'part_name_x': 'part_name',
        'material_number_x': 'material_number',
    }, inplace=True
    )
    all_valid = all_valid.drop(['has_high_spare', 'high_spare', 'part_name', 'material_number_y', 'standard_cost_y', 'part_name_y'], 1)

    # Remove the rows for item which are not present in SAP file ,error condition 1
    all_valid = all_valid[all_valid['Product Ordering Name'].isin(unique_parts_in_sap)]

    # if a given Depot is not in SAP inventory file then it an Error BUT we can still process this.
    # Essentially they need to work with a partner to open a depot (Error 4)

    unique_depot_in_sap = sap_inventory['Storage Location = Depot Name'].unique()
    depot_not_in_sap_file = all_valid[~all_valid['node_depot_belongs'].isin(unique_depot_in_sap)]
    if not depot_not_in_sap_file.empty:
        depot_not_in_sap_file['depot_in_sap_file'] = False  # flag used in finding error 4
        process_error_pon('error_records', depot_not_in_sap_file, analysis_date, analysis_id)

    to_sql_current_inventory('current_inventory', sap_inventory, analysis_date, analysis_id)

    update_prospect_step(prospect_id, 4, analysis_date)  # Dump sap_inventory Table Status
    return all_valid, parts, get_ratio_to_pon, depot, high_spares, standard_cost


def shared_function_for_bom_record(bom_file, sap_file, analysis_date, analysis_id, prospect_id, replenish_time):

    # 5.2 Capture the data from the file in PON-Depot and Inventory values.
    # Note some of these parts may not be sparable and will perform such checks later.
    bom_df = read_bom_file(bom_file)

    # Save BOM record data in table
    to_sql_bom_record('bom_record', bom_df.copy(), analysis_date, analysis_id)

    update_prospect_step(prospect_id, 2, analysis_date)  # Dump customer_dna Table Status

    # 5.3 Capture SAP Export and load into current inventory
    convert_headers_in_sap_file(sap_file)
    update_prospect_step(prospect_id, 3, analysis_date)

    sap_inventory = read_sap_export_file(sap_file)
    to_sql_current_inventory('current_inventory', sap_inventory.copy(), analysis_date, analysis_id)
    update_prospect_step(prospect_id, 4, analysis_date)  # Dump sap_inventory Table Status

    # 5.4 Load key data elements in data frame:: Standard cost table,
    # Unspared pon table , High spares table (Substitution matrix data)

    (misnomer_pons, standard_cost, node, spared_pons, highspares, get_ratio_to_pon, parts,
     parts_cost, high_spares, depot) = fetch_db(replenish_time)

    # Section 5.7 validate_PON & validate_depot
    # This step checks if PON has invalid names and Depots have valid names.
    # Invalid ones need to be logged as DNA Input error warning.

    valid_pon = validate_pon_for_bom(bom_df, analysis_date, analysis_id)
    valid_pon = validate_depot_for_bom(valid_pon, analysis_date, analysis_id)

    # Keep only sparable PON
    valid_pon['is_sparrable'] = False
    valid_pon = pd.merge(valid_pon, spared_pons, left_on=['Product Ordering Name'], right_on=['part_name'], how='inner')
    valid_pon.loc[(valid_pon['Product Ordering Name'] == valid_pon['part_name']), 'is_sparrable'] = True
    # Remove unnecessary column generated by merge
    valid_pon = valid_pon.drop(['part_name'], 1)

    # Keep only sparable pons
    valid_pon = valid_pon[valid_pon['is_sparrable'] == True]

    # Keep only parts which has standard_cost
    valid_pon['has_std_cost'] = False
    valid_pon = pd.merge(valid_pon, standard_cost, left_on=['Product Ordering Name'], right_on=['part_name'], how='inner')
    valid_pon.loc[(valid_pon['standard_cost'].notna()), 'has_std_cost'] = True

    # Remove unnecessary column generated by merge
    valid_pon = valid_pon.drop(['part_name', 'material_number'], 1)

    # Keep only pons with std_cost
    valid_pon = valid_pon[valid_pon['has_std_cost'] == True]

    # Get High spares of valid PONS

    valid_pon['has_high_spare'] = False
    all_valid = pd.merge(valid_pon, high_spares, left_on=['Product Ordering Name'], right_on=['part_name'], how='left')


    # Remove unnecessary column generated by merge
    all_valid = all_valid.drop(['part_name'], 1)

    all_valid.loc[(all_valid['high_spare'].notna()), 'has_high_spare'] = True

    # if item is high spare & high spare not in SAP file, Remove such rows

    # Get unique parts in SAP
    # keep only valid rows, keep rows having part_names are present in sap_inventory

    unique_parts_in_sap = sap_inventory['Material Description = Part Name'].unique()

    high_spares_not_in_sap = all_valid[~all_valid['has_high_spare'] == True & all_valid['high_spare'].isin(unique_parts_in_sap)]

    # Log error condition 2, high spare of item are not in SAP file
    if not high_spares_not_in_sap.empty:
        keep_col = ['Product Ordering Name', 'high_spare']
        high_spares_not_in_sap = high_spares_not_in_sap[keep_col]
        high_spares_not_in_sap.rename(columns={
            'Product Ordering Name': 'PON'
        }, inplace=True
        )

        high_spares_not_in_sap.loc[:, 'analysis_request_time'] = analysis_date
        high_spares_not_in_sap.loc[:, 'cust_id'] = 7
        high_spares_not_in_sap.loc[:, 'request_id'] = analysis_id
        for index, row in high_spares_not_in_sap.iterrows():
            high_spares_not_in_sap.loc[index, 'error_reason'] = 'High Spare {0} for Part {1} not present in SAP file'.format(row['high_spare'], row['PON'])

        high_spares_not_in_sap = high_spares_not_in_sap.drop(['high_spare'], 1)
        high_spares_not_in_sap.to_sql(name='error_records', con=engine, index=False, if_exists='append')

        print("Loaded Data into table : {0}".format('error_records'))

    # We logged error condition,now remove those rows
    all_valid = all_valid[all_valid['has_high_spare'] == True & all_valid['high_spare'].isin(unique_parts_in_sap)]

    # Find the parts which are not in SAP file & log error condition 1
    not_in_sap_file = all_valid[~all_valid['Product Ordering Name'].isin(unique_parts_in_sap)]

    if not not_in_sap_file.empty:
        keep_col = ['Product Ordering Name']
        not_in_sap_file = not_in_sap_file[keep_col]
        not_in_sap_file.rename(columns={
            'Product Ordering Name': 'PON'
        }, inplace=True
        )
        not_in_sap_file.loc[:, 'analysis_request_time'] = analysis_date
        not_in_sap_file.loc[:, 'cust_id'] = 7
        not_in_sap_file.loc[:, 'request_id'] = analysis_id
        for index, row in not_in_sap_file.iterrows():
            not_in_sap_file.loc[index, 'error_reason'] = 'Part {0} not present in SAP file'.format(row['PON'])

        not_in_sap_file.to_sql(name='error_records', con=engine, index=False, if_exists='append')
        print("Loaded Data into table : {0}".format('error_records'))

    # Remove the rows for item which are not present in SAP file ,error condition 1
    all_valid = all_valid[all_valid['Product Ordering Name'].isin(unique_parts_in_sap)]

    # Remove rows which has high spares ,but high spares do not have std_cost
    all_valid = pd.merge(all_valid, standard_cost, left_on='high_spare', right_on='part_name', how='left')

    high_spare_no_std_cost = all_valid[all_valid['has_high_spare'] == True & all_valid['standard_cost_y'].isna()]

    all_valid = all_valid[all_valid['has_high_spare'] == True & all_valid['standard_cost_y'].notna()]
    all_valid = all_valid.drop(['material_number', 'standard_cost_y', 'part_name'], 1)

    if not high_spare_no_std_cost.empty:
        keep_col = ['Product Ordering Name']
        high_spare_no_std_cost = high_spare_no_std_cost[keep_col]
        high_spare_no_std_cost.rename(columns={
            'Product Ordering Name': 'PON'
        }, inplace=True
        )
        high_spare_no_std_cost.loc[:, 'analysis_request_time'] = analysis_date
        high_spare_no_std_cost.loc[:, 'cust_id'] = 7
        high_spare_no_std_cost.loc[:, 'request_id'] = analysis_id
        for index, row in high_spare_no_std_cost.iterrows():
            high_spare_no_std_cost.loc[index, 'error_reason'] = 'High Spare for Part {0} do not have standard cost'.format(row['PON'])

        high_spare_no_std_cost.to_sql(name='error_records', con=engine, index=False, if_exists='append')
        print("Loaded Data into table : {0}".format('error_records'))

    # if a given Depot is not in SAP inventory file then it an Error BUT we can still process this.
    # Essentially they need to work with a partner to open a depot (Error 4)

    unique_depot_in_sap = sap_inventory['Storage Location = Depot Name'].unique()
    depot_not_in_sap_file = all_valid[~all_valid['node_depot_belongs'].isin(unique_depot_in_sap)]

    if not depot_not_in_sap_file.empty:
        keep_col = ['Product Ordering Name', 'node_depot_belongs']
        depot_not_in_sap_file = depot_not_in_sap_file[keep_col]
        depot_not_in_sap_file.rename(columns={
            'Product Ordering Name': 'PON'
        }, inplace=True
        )
        depot_not_in_sap_file.loc[:, 'analysis_request_time'] = analysis_date
        depot_not_in_sap_file.loc[:, 'cust_id'] = 7
        depot_not_in_sap_file.loc[:, 'request_id'] = analysis_id
        for index, row in depot_not_in_sap_file.iterrows():
            depot_not_in_sap_file.loc[index, 'error_reason'] = 'Depot {0} for Part {1} not present in SAP file'.format(row['node_depot_belongs'], row['PON'])

        depot_not_in_sap_file = depot_not_in_sap_file.drop(['node_depot_belongs'], 1)
        depot_not_in_sap_file.to_sql(name='error_records', con=engine, index=False, if_exists='append')
        print("Loaded Data into table : {0}".format('error_records'))

    return all_valid, parts, get_ratio_to_pon, depot, high_spares, standard_cost


def bom_calcuation(dna_file, sap_file, analysis_date, analysis_id, prospect_id, replenish_time, is_inservice_only, item_category, product_category, product_family, product_phase, product_type):

    all_valid, parts, get_ratio_to_pon, depot, high_spares, standard_cost = shared_function(dna_file, sap_file,
                                                                                            analysis_date, analysis_id,
                                                                                            prospect_id, replenish_time,
                                                                                            is_inservice_only, item_category,
                                                                                            product_category, product_family,
                                                                                            product_phase, product_type)

    Get_Fru = pd.DataFrame(
        all_valid.groupby(['Product Ordering Name', 'node_depot_belongs'])['node_depot_belongs'].count())
    Get_Fru.to_csv(Configuration.fruc_file_location, index=True)
    Get_Fru = pd.read_csv(Configuration.fruc_file_location)
    Get_Fru = Get_Fru.rename(columns={'node_depot_belongs.1': 'count'})
    Get_Fru.groupby(['Product Ordering Name', 'node_depot_belongs'])['count'].last().unstack(
        fill_value=0).stack().to_csv(Configuration.bom_table, header=True)
    get_bom_for_table = pd.read_csv(Configuration.bom_table)
    get_bom_for_table = get_bom_for_table.rename(columns={'0': 'PON Quanity'})
    #get_bom_for_table.to_csv("/Users/anup/eKryp/infinera/Parts-Analysis/data/install_base.csv", index=False)
    to_sql_current_ib('current_ib', get_bom_for_table, analysis_id)

    get_bom_for_table.rename(columns={
        'pon_quanity': 'PON Quanity',
        'product_ordering_name': 'Product Ordering Name'
    }, inplace=True
    )
    get_bom_for_table.drop(['request_id'], 1, inplace=True)
    return get_bom_for_table, get_ratio_to_pon, parts, depot, high_spares, standard_cost
    print('BOM calculation complete')


def bom_calcuation_for_bom_records(bom_file, sap_file, analysis_date, analysis_id, prospect_id, replenish_time):

    all_valid, parts, get_ratio_to_pon, depot, high_spares, standard_cost = shared_function_for_bom_record(bom_file, sap_file, analysis_date,
                                                                                                           analysis_id, prospect_id, replenish_time)

    '''
    Install base PON quantity logic change for BOM file as BOM
    already has PON quantity we will use that one 
    Get_Fru = pd.DataFrame(
        all_valid.groupby(['Product Ordering Name', 'node_depot_belongs'])['node_depot_belongs'].count())
    Get_Fru.to_csv(Configuration.fruc_file_location, index=True)
    Get_Fru = pd.read_csv(Configuration.fruc_file_location)
    Get_Fru = Get_Fru.rename(columns={'node_depot_belongs.1': 'count'})
    Get_Fru.groupby(['Product Ordering Name', 'node_depot_belongs'])['count'].last().unstack(
        fill_value=0).stack().to_csv(Configuration.bom_table, header=True)
    get_bom_for_table = pd.read_csv(Configuration.bom_table)
    get_bom_for_table = get_bom_for_table.rename(columns={'0': 'PON Quanity'})
    '''
    get_bom_for_table = all_valid[['Product Ordering Name', 'node_depot_belongs', 'PON Quantity']]
    get_bom_for_table = get_bom_for_table.rename(columns={'PON Quantity': 'PON Quanity'})
    #get_bom_for_table.to_csv("/Users/anup/eKryp/infinera/Parts-Analysis/data/install_base.csv", index=False)
    to_sql_current_ib('current_ib', get_bom_for_table, analysis_id)
    get_bom_for_table.rename(columns={
        'pon_quanity': 'PON Quanity',
        'product_ordering_name': 'Product Ordering Name'
    }, inplace=True
    )
    get_bom_for_table.drop(['request_id'], 1, inplace=True)
    return get_bom_for_table, get_ratio_to_pon, parts, depot, high_spares, standard_cost
    print('BOM calculation complete')


def simple_calculation(get_bom_for_table):
    get_bom_for_table.loc[get_bom_for_table['PON Quanity'] > 0, 'PON Quanity'] = 1
    get_bom_for_table.replace(np.nan, 0, inplace=True)
    get_bom_for_table = get_bom_for_table[['Product Ordering Name', 'node_depot_belongs', 'PON Quanity']]
    print("Simple Calculation")
    # print(get_bom_for_table)
    print("End Simple Calculation")
    return get_bom_for_table


def mtbf_calculation(get_bom_for_table, get_ratio_to_pon, parts, analysis_date, analysis_id):
    spare_cols = [str(x + 1) for x in range(10)]

    def find_spare_bin(row):
        bins = [0] + list(row[spare_cols])
        # Check for empyt count, if there is no calss family for PON
        # Then make required spared = 1, the logic is make the first column == FRU count
        # the return spare would be 1
        bins = [row['PON Quanity'] if math.isnan(x) else x for x in bins]
        return np.digitize(row['PON Quanity'], bins, right=True)

    Get_MTBF_BOM = pd.merge(get_bom_for_table, parts, left_on='Product Ordering Name', right_on='part_name', how='left')
    Get_MTBF_BOM = Get_MTBF_BOM[
        ['Product Ordering Name', 'node_depot_belongs', 'PON Quanity', 'part_reliability_class']]
    Get_MTBF_BOM = pd.merge(Get_MTBF_BOM, get_ratio_to_pon, left_on='part_reliability_class', right_on='product_family',
                            how='left')

    # If the reliability class is not found for a PON then we will assign a default count of 1
    # Process such records but error out condition 6

    reliabilty_class_missing = Get_MTBF_BOM[Get_MTBF_BOM['part_reliability_class'].isna()]
    if not reliabilty_class_missing.empty:
        keep_col = ['Product Ordering Name']
        reliabilty_class_missing = reliabilty_class_missing[keep_col]
        reliabilty_class_missing.rename(columns={
            'Product Ordering Name': 'PON'
        }, inplace=True
        )
        reliabilty_class_missing['error_reason'] = 'Part has no associated reliablity class'
        reliabilty_class_missing.loc[:, 'analysis_request_time'] = analysis_date
        reliabilty_class_missing.loc[:, 'cust_id'] = 7
        reliabilty_class_missing.loc[:, 'request_id'] = analysis_id
        reliabilty_class_missing.to_sql(name='error_records', con=engine, index=False, if_exists='append')
        print("Loaded Data into table : {0}".format('error_records'))

    Get_MTBF_BOM.loc[(Get_MTBF_BOM['part_reliability_class'].isna(), 'PON Quanity')] = 1

    Get_MTBF_BOM['PON Quanity'] = Get_MTBF_BOM.apply(find_spare_bin, axis=1)
    Get_MTBF_BOM_calc = Get_MTBF_BOM[['Product Ordering Name', 'node_depot_belongs', 'PON Quanity']]

    print("MTBF Calculation")
    # print(Get_MTBF_BOM_calc)
    print("End MTBF Calculation")
    return Get_MTBF_BOM_calc


def remove_hub_depot(df, depot):
    all_depots = pd.merge(df, depot, left_on='node_depot_belongs', right_on='depot_name', how='left')

    # PONs depots are HUB,hub=1 means they are HUB ,0 means they are not hub

    # Remove the PON which are in the below list
    # Make Pon quantity = 0 for PON in below list & their depot are not hub
    pon_list = ["DTC-ANSI-B=", "DTC-ETSI-B=", "OTC-ANSI-A=", "OTC-ETSI-A=", "XTC-2", "XTC-4",
                "XTC-10", "XTC-2E", "MTC-9-B", "MTC-6", "MPC-6", "MTC-9", "MTC-ANSI="]
    # Changed condition to all_depots['hub'] != 1 from all_depots['hub'] == 0 as depot_name in depot table has null values as well
    # Hence we are only interested in non hub rows & all_depots['hub'] != 1 gives those rows
    all_depots.loc[(all_depots['Product Ordering Name'].isin(pon_list)) & (all_depots['hub'] != 1), 'PON Quanity'] = 0

    # Keep only required columns
    all_depots = all_depots[['Product Ordering Name', 'node_depot_belongs', 'PON Quanity']]
    return all_depots

def calculate_shared_depot(single_bom, high_spares, standard_cost, parts, analysis_date, user_email_id, analysis_id, customer_name):

    '''
    step 1. first get parts and its high spare
    step 2. check if given part's quantity is !=0 if it not equal to 0 retain the value
    step 3. if given PON's quantity is 0 then get quantity from high spares
    step 4. quantity is either reorder point or total stock
    '''

    Connection = Configuration.ECLIPSE_DATA_DB_URI
    # step 1 get PON and its high spares - we will need
    # given_Spare name, high_spare_name, total_order_given, total_order_high, reorder_give, reorder_high_spare

    #get_zinventory_sql = 'SELECT storage_location,material_desc,total_stock,reorder_point FROM sap_inventory '
    #z_inventory = read_sap_export_file()
    get_zinventory_sql = 'SELECT storage_location,part_name as material_desc,total_stock,reorder_point FROM ' \
                         'current_inventory where request_id={}'.format(analysis_id)
    z_inventory = read_data(get_zinventory_sql, Connection)
    z_inventory.rename(columns={
        'storage_location': 'Storage Location',
        'material_desc': 'Material Description',
        'total_stock': 'Total Stock',
        'reorder_point': 'Reorder Point'
    }, inplace=True
    )

    ''' This step is important because, when the inventory doesn't have reorder or total stock, the value is replaced - if Highs spare exists with
       high spare qty value if not replcae it with 0, but when we merge, the qty is null and the depot won't show up and grabbing value from high spare
       won't be possible, hence this step. '''

    '''
    This step gives us starting inventory
    '''
    # check if process 3 already stores the total inventory in databse then change the follwing line
    # to read from database instead of file -- For Ashish
    z_inventory.groupby(['Material Description', 'Storage Location'])['Total Stock', 'Reorder Point'].sum().unstack(
        fill_value=0).stack().to_csv(Configuration.shared_depot_file, header=True)
    sub = pd.read_csv(Configuration.shared_depot_file)

    # this step is to make sure that we take into account those depot that are present in the input file
    # but absent in inventory in which case all the qty in shared depot for missing inventory depot is marked zero

    #shared_depot = pd.merge(single_bom, z_inventory, left_on=['part_name','depot_name'], right_on=['Material Description','Storage Location'], how = 'left')
    shared_depot = single_bom

    # if the depot name is empty mark it with first occuring depot, set 0 to qty

    shared_depot = pd.merge(shared_depot, high_spares, left_on=['part_name'], right_on=['part_name'], how='left').merge(
        sub, left_on=['part_name', 'depot_name'], right_on=['Material Description', 'Storage Location'], how='left')

    shared_depot = pd.merge(shared_depot, sub, left_on=['high_spare', 'depot_name'], right_on=['Material Description', 'Storage Location'], how='left')
    shared_depot = shared_depot.replace(np.nan, 0)

    idx = (shared_depot['high_spare'] != 0)
    shared_depot.loc[idx, 'is_high_spares'] = True

    shared_depot = shared_depot.replace(np.nan, 0)

    shared_depot_total = shared_depot[['Total Stock_x', 'part_name', 'high_spare', 'Material Description_x', 'Total Stock_y', 'depot_name','pon_quantity','is_high_spares']]
    shared_depot_reorder = shared_depot[['Reorder Point_x', 'part_name', 'high_spare', 'Material Description_x', 'Reorder Point_y', 'depot_name','pon_quantity','is_high_spares']]

    # only for for those pons that have high pons check if pon,s qty is 0, if 0 then grab shared depot qty
    # else keep depot qty

    shared_depot_total['Total Stock'] = shared_depot_total['Total Stock_x']
    idx = (shared_depot_total['Total Stock_x'] == 0)
    idx_pon_qty = (shared_depot_total['pon_quantity'] > 0)

    # set a flag to check if PON is 0 and another flag to check index of IB
    #shared_depot_total.loc[idx, 'using_highspare_for_totalstock'] = True

    shared_depot_total.loc[idx, 'is_inventory_zero'] = True
    shared_depot_total.loc[idx_pon_qty, 'has_IB'] = True

    shared_depot_total.loc[
        ((shared_depot_total['is_inventory_zero'] == True) & (
                    shared_depot_total['has_IB'] == True)), 'highspare_count_for_totalstock'] = shared_depot_total['Total Stock_y']
    shared_depot_total.loc[idx, 'Total Stock'] = shared_depot_total.loc[idx, 'Total Stock_y']

    
    shared_depot_reorder['Reorder Point'] = shared_depot_reorder['Reorder Point_x']
    idx = (shared_depot_reorder['Reorder Point_x'] == 0)
    shared_depot_reorder.loc[idx, 'is_inventory_zero'] = True
    shared_depot_reorder.loc[idx_pon_qty, 'has_IB'] = True


    shared_depot_reorder.loc[
        ((shared_depot_reorder['is_inventory_zero'] == True) & (
                    shared_depot_reorder['has_IB'] == True)), 'highspare_count_for_reorderpoint'] = shared_depot_reorder['Reorder Point_y']
    shared_depot_reorder.loc[idx, 'Reorder Point'] = shared_depot_reorder.loc[idx, 'Reorder Point_y']

    
    shared_depot_total = shared_depot_total[['part_name', 'Total Stock', 'depot_name','highspare_count_for_totalstock']]
    shared_depot_reorder = shared_depot_reorder[['part_name', 'Reorder Point', 'depot_name','is_high_spares','highspare_count_for_reorderpoint']]

    shared_depot = pd.merge(shared_depot_reorder, shared_depot_total, on=['part_name','depot_name'])

    single_bom = pd.merge(single_bom, shared_depot, on=['part_name', 'depot_name'])

    # if simple is selected
    # single_bom.loc[(single_bom['pon_quantity'] > 0), 'shared_quantity'] = single_bom['pon_quantity']
    # else when mtbf_bom is selected
    single_bom['shared_quantity'] = single_bom['pon_quantity']
    single_bom['net_total_stock'] = np.where(single_bom['shared_quantity'] - single_bom['Total Stock'] > 0, single_bom['shared_quantity'] - single_bom['Total Stock'], 0)
    single_bom['net_reorder_point'] = np.where(single_bom['shared_quantity'] - single_bom['Reorder Point'] > 0,single_bom['shared_quantity'] - single_bom['Reorder Point'], 0)

    # Get Part_number for summary table
    single_bom = pd.merge(single_bom, parts, on='part_name', how='left')
    single_bom = single_bom[['part_name', 'depot_name', 'Total Stock', 'Reorder Point',
                             'is_high_spares', 'shared_quantity', 'material_number', 'net_total_stock' , 'net_reorder_point','highspare_count_for_totalstock','highspare_count_for_reorderpoint']]

    # Get Part_Cost for summary table

    single_bom = pd.merge(single_bom, standard_cost, on='material_number', how='left')
    single_bom = single_bom[['part_name_x', 'depot_name', 'Total Stock', 'Reorder Point',
                             'is_high_spares', 'shared_quantity', 'material_number', 'net_total_stock', 'net_reorder_point', 'standard_cost','highspare_count_for_totalstock','highspare_count_for_reorderpoint']]

    single_bom['net_total_stock_cost'] = single_bom['net_total_stock'] * single_bom['standard_cost']
    single_bom['net_reorder_point_cost'] = single_bom['net_reorder_point'] * single_bom['standard_cost']
    # calculate high spare cost
    single_bom['High_spare_totalstock_cost'] = single_bom['highspare_count_for_totalstock'] * single_bom[
        'standard_cost']
    single_bom['High_spare_reoderpoint_cost'] = single_bom['highspare_count_for_reorderpoint'] * single_bom[
        'standard_cost']

    single_bom = single_bom.fillna(0)

    single_bom.rename(columns={
        'part_name_x': 'part_name',
        'is_high_spares':'high_spare',
        'Reorder Point':'reorder_point',
        'Total Stock':'total_stock',
        'highspare_count_for_totalstock':'used_spare_count_total_stock',
        'highspare_count_for_reorderpoint': 'used_spare_count_reorder'
    }, inplace=True
    )

    single_bom.loc[:, 'cust_id'] = 7
    # single_bom.loc[:, 'analysis_request_time'] = analysis_date
    # single_bom.loc[:, 'user_email_id'] = user_email_id
    single_bom.loc[:, 'request_id'] = analysis_id
    single_bom.loc[:, 'customer_name'] = customer_name

    # Make previous records for customer as not latest is_latest='N'
    # & new records getting inserted are by default is_latest='Y'

    engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args)
    query = "update summary set is_latest='N' where customer_name='{0}'".format(customer_name)
    print(query)
    engine.execute(query)
    single_bom.to_sql(name='summary', con=engine, index=False, if_exists='append')
    print("Loaded data into summary table")

    # Initially make shared_
    # quantiity for all PON as 0,
    #single_bom['shared_quantity'] = 0
    #single_bom['is_high_spares'] = False
    # For PON in bom whose pon_quantity > 0 and has not having high spares
    # make shared quantity as bom explosion quantity
    #single_bom.loc[(single_bom['pon_quantity'] > 0) & (single_bom['high_spare'].isna()), 'shared_quantity'] = single_bom['pon_quantity']

    # For PON in bom whose pon_quantity > 0 and has having high spares
    # and not present in zinventory
    # make shared quantity as bom explosion quantity

    #single_bom.loc[(single_bom['pon_quantity'] > 0) & (single_bom['high_spare'].notnull()) & (single_bom['storage_location'].isna()), 'shared_quantity'] = single_bom['pon_quantity']

    # For PON in bom whose pon_quantity > 0 and has having high spares
    # and present in zinventory
    # check spared_part in present in same depot as bom & zinventory
    # make shared quantity as bom explosion quantity
    '''

    single_bom = single_bom[['part_name', 'depot_name', 'high_spare', 'total_stock', 'reorder_point', 'is_high_spares', 'shared_quantity']]
    single_bom['net_total_stock'] = single_bom['total_stock'] - single_bom['shared_quantity']
    single_bom['net_reorder_point'] = single_bom['reorder_point'] - single_bom['shared_quantity']

    # Get Part_number for summary table
    single_bom = pd.merge(single_bom, parts, on='part_name', how='left')
    single_bom = single_bom[['part_name', 'depot_name', 'total_stock', 'reorder_point',
                             'is_high_spares', 'shared_quantity', 'material_number', 'net_total_stock'
                             , 'net_reorder_point']]

    # Get Part_Cost for summary table

    single_bom = pd.merge(single_bom, standard_cost, on='material_number', how='left')
    single_bom = single_bom[['part_name_x', 'depot_name', 'total_stock', 'reorder_point',
                             'is_high_spares', 'shared_quantity', 'material_number','net_total_stock'
                             , 'net_reorder_point', 'standard_cost']]

    single_bom['net_total_stock_cost'] = single_bom['net_total_stock'] * single_bom['standard_cost']
    single_bom['net_reorder_point_cost'] = single_bom['net_reorder_point'] * single_bom['standard_cost']
    single_bom.rename(columns={
        'part_name_x': 'part_name',
        'is_high_spares': 'high_spare'
    }, inplace=True
    )
    single_bom['cust_id'] = 7
    single_bom.to_sql(name='summary', con=engine, index=False, if_exists='append')
    print("Loaded data into summary table")'''

'''  
def calculate_shared_depot(single_bom, high_spares, standard_cost, parts, analysis_date, user_email_id, analysis_id, customer_name):

    Connection = Configuration.ECLIPSE_DATA_DB_URI
    single_bom = pd.merge(single_bom, high_spares, on='part_name', how='left')
    get_zinventory_sql = 'SELECT storage_location,material_desc,total_stock,reorder_point FROM ' \
                         'sap_inventory where request_id={}'.format(analysis_id)
    z_inventory = read_data(get_zinventory_sql, Connection)
    single_bom = pd.merge(single_bom, z_inventory, left_on=['part_name', 'depot_name'],
                          right_on=['material_desc', 'storage_location'], how='left')

    # Initially make shared_quantiity for all PON as 0,
    single_bom['shared_quantity'] = 0
    single_bom['is_high_spares'] = False
    # For PON in bom whose pon_quantity > 0 and has not having high spares
    # make shared quantity as bom explosion quantity
    single_bom.loc[(single_bom['pon_quantity'] > 0) & (single_bom['high_spare'].isna()), 'shared_quantity'] = \
    single_bom['pon_quantity']

    # For PON in bom whose pon_quantity > 0 and has having high spares
    # and not present in zinventory
    # make shared quantity as bom explosion quantity

    single_bom.loc[(single_bom['pon_quantity'] > 0) & (single_bom['high_spare'].notnull()) & (
    single_bom['storage_location'].isna()), 'shared_quantity'] = single_bom['pon_quantity']

    # For PON in bom whose pon_quantity > 0 and has having high spares
    # and present in zinventory
    # check spared_part in present in same depot as bom & zinventory
    # make shared quantity as bom explosion quantity
    single_bom.loc[(single_bom['pon_quantity'] > 0) & (single_bom['high_spare'].notnull()) & (
    single_bom['storage_location'].notnull()) & (
                   single_bom['depot_name'] == single_bom['storage_location']), 'shared_quantity'] = single_bom[
        'pon_quantity']
    single_bom.loc[(single_bom['total_stock'].isna()), 'total_stock'] = 0
    single_bom.loc[(single_bom['reorder_point'].isna()), 'reorder_point'] = 0
    single_bom.loc[(single_bom['high_spare'].notnull()), 'is_high_spares'] = True

    single_bom = single_bom[
        ['part_name', 'depot_name', 'high_spare', 'total_stock', 'reorder_point', 'is_high_spares', 'shared_quantity']]
    single_bom['net_total_stock'] = single_bom['total_stock'] - single_bom['shared_quantity']
    single_bom['net_reorder_point'] = single_bom['reorder_point'] - single_bom['shared_quantity']

    # Get Part_number for summary table
    single_bom = pd.merge(single_bom, parts, on='part_name', how='left')
    single_bom = single_bom[['part_name', 'depot_name', 'total_stock', 'reorder_point',
                             'is_high_spares', 'shared_quantity', 'material_number', 'net_total_stock'
        , 'net_reorder_point']]

    # Get Part_Cost for summary table

    single_bom = pd.merge(single_bom, standard_cost, on='material_number', how='left')
    single_bom = single_bom[['part_name_x', 'depot_name', 'total_stock', 'reorder_point',
                             'is_high_spares', 'shared_quantity', 'material_number', 'net_total_stock'
        , 'net_reorder_point', 'standard_cost']]

    single_bom['net_total_stock_cost'] = single_bom['net_total_stock'] * single_bom['standard_cost']
    single_bom['net_reorder_point_cost'] = single_bom['net_reorder_point'] * single_bom['standard_cost']
    single_bom.rename(columns={
        'part_name_x': 'part_name',
        'is_high_spares': 'high_spare'
    }, inplace=True
    )
    #single_bom['cust_id'] = 7
    single_bom.loc[:, 'cust_id'] = 7
    single_bom.loc[:, 'analysis_request_time'] = analysis_date
    single_bom.loc[:, 'user_email_id'] = user_email_id
    single_bom.loc[:, 'request_id'] = analysis_id
    single_bom.loc[:, 'customer_name'] = customer_name
    single_bom.to_sql(name='summary', con=engine, index=False, if_exists='append')
    print("Loaded data into summary table")
    
'''


def get_bom(dna_file, sap_file, analysis_date, analysis_id, prospect_id, replenish_time, is_mtbf, is_inservice_only, item_category, product_category, product_family, product_phase, product_type):

    bom, get_ratio_to_pon, parts, depot, high_spares, standard_cost = bom_calcuation(dna_file, sap_file,
                                                                                     analysis_date, analysis_id,
                                                                                     prospect_id, replenish_time,
                                                                                     is_inservice_only, item_category,
                                                                                     product_category, product_family,
                                                                                     product_phase, product_type)

    # Flag will be there to choose from simple or mtbf calculation.

    if is_mtbf.lower() == 'no':
        print("Simple BOM getting executed")
        gross_depot = simple_calculation(bom)

        # 5.13 Accommodating for Corporate and Regional Disti - Process 13
    
        gross_depot = remove_hub_depot(gross_depot, depot)
        gross_depot_hnad = add_hnad(gross_depot, quantity=1)
        to_sql_bom('mtbf_bom_calculated', gross_depot_hnad, analysis_date, analysis_id)
        return gross_depot_hnad, high_spares, standard_cost, parts

    elif is_mtbf.lower() == 'yes':
        print("MTBF BOM getting executed")
        gross_depot = mtbf_calculation(bom, get_ratio_to_pon, parts, analysis_date, analysis_id)

        #5.13 Accommodating for Corporate and Regional Disti - Process 13

        gross_depot = remove_hub_depot(gross_depot, depot)
        gross_depot_hnad = add_hnad(gross_depot, quantity=1)
        to_sql_mtbf('mtbf_bom_calculated', gross_depot_hnad, analysis_date, analysis_id)
        return gross_depot_hnad, high_spares, standard_cost, parts


def get_bom_for_bom_record(bom_file, sap_file, analysis_date, analysis_id, prospect_id, replenish_time, is_mtbf):

    bom, get_ratio_to_pon, parts, depot, high_spares, standard_cost = bom_calcuation_for_bom_records(bom_file, sap_file,
                                                                                     analysis_date, analysis_id,
                                                                                     prospect_id, replenish_time)

    # Flag will be there to choose from simple or mtbf calculation.
    if is_mtbf.lower() == 'no':
        print("Simple BOM getting executed")
        gross_depot = simple_calculation(bom)

    # 5.13 Accommodating for Corporate and Regional Disti - Process 13

        gross_depot = remove_hub_depot(gross_depot, depot)
        gross_depot_hnad = add_hnad(gross_depot, quantity=1)
        to_sql_bom('mtbf_bom_calculated', gross_depot_hnad, analysis_date, analysis_id)
        return gross_depot_hnad, high_spares, standard_cost, parts

    elif is_mtbf.lower() == 'yes':
        print("MTBF BOM getting executed")
        gross_depot = mtbf_calculation(bom, get_ratio_to_pon, parts, analysis_date, analysis_id)

        # 5.13 Accommodating for Corporate and Regional Disti - Process 13

        gross_depot = remove_hub_depot(gross_depot, depot)
        gross_depot_hnad = add_hnad(gross_depot, quantity=1)
        to_sql_mtbf('mtbf_bom_calculated', gross_depot_hnad, analysis_date, analysis_id)
        return gross_depot_hnad, high_spares, standard_cost, parts


def convert_headers_in_sap_file(sap_file):

    sap_inventory_data = pd.read_excel(sap_file, sheet_name='Sheet1')

    our_columns = ['Plant', 'Storage Location = Depot Name', 'Material Number', 'Material Description = Part Name',
               'Total Stock', 'Reorder Point', 'Standard Cost', 'Total Standard Cost', 'STO - Qty To be Dlv.',
               'Delivery - Qty To be Dlv.']

    infinera_columns = ['Material Number', 'Material Description', 'Plant', 'Storage Location',
                        'Reorder Point', 'Total Stock', 'Standard Cost', 'Total Standard Cost',
                        'STO - Qty To be Dlv.', 'Delivery - Qty To be Dlv.']
    sap_inventory_data.rename(columns={
            'Material Description': 'Material Description = Part Name',
            'Storage Location': 'Storage Location = Depot Name',
                            }, inplace=True
                            )
    sap_inventory_data[our_columns].to_excel(sap_file, index=False)


class Email(Resource):
    senderEmailAddress = ""
    recevierEmailAddress = ""
    emailSubject = ""
    emailMessage = ""

    def __init__(self, senderEmailAddress, recevierEmailAddress, emailSubject, emailMessage ):
        self.senderEmailAddress = senderEmailAddress
        self.recevierEmailAddress = recevierEmailAddress
        self.emailSubject = emailSubject
        self.emailMessage = emailMessage



def sendEmailNotificatio(user_email_id,subject,message):
    print('calling email method')
    request = Email(senderEmailAddress="noreply@ekryp.com",recevierEmailAddress=user_email_id,emailSubject=subject,emailMessage=message)
    dumps = json.dumps(request.__dict__)
    jsondata = json.loads(dumps)
    print('JSON dic ----->',jsondata)
    response = requests.post("http://mailgun:5001/api/mail/send",json=jsondata)
    print('email response ----->',response.content)


@celery.task
def derive_table_creation(dna_file, sap_file, analysis_date, user_email_id, analysis_id, customer_name, prospect_id, replenish_time, analysis_name, is_mtbf, is_inservice_only, item_category, product_category, product_family, product_phase, product_type):
   
    try:
        sendEmailNotificatio(user_email_id, " Infinera Analysis ", " Your "+analysis_name+" Analysis Submitted Successfully..")
        convert_headers_in_sap_file(sap_file)
        def set_request_status(status, analysis_id,msg):
            engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args)
            query = "update analysis_request set requestStatus='{0}',failure_reason='{2}' " \
                "where analysis_request_id = {1}".format(status, analysis_id,msg)
            print(query)
            engine.execute(query)

        single_bom, high_spares, standard_cost, parts = get_bom(dna_file, sap_file, analysis_date, analysis_id, prospect_id, replenish_time, is_mtbf, is_inservice_only, item_category, product_category, product_family, product_phase, product_type)
        update_prospect_step(prospect_id, 5, analysis_date)  # BOM calculation Status
        calculate_shared_depot(single_bom, high_spares, standard_cost, parts, analysis_date,
                           user_email_id, analysis_id, customer_name)

        update_prospect_step(prospect_id, 6, analysis_date)  # Summary Calculation  Status
        set_request_status('Completed', analysis_id, 'Success')
        sendEmailNotificatio(user_email_id, " Infinera Analysis ", "Your "+analysis_name+" Analysis Completed Successfully..")
    except CustomException as e:
        sendEmailNotificatio(user_email_id, " Infinera Analysis ", " Your "+analysis_name+" Analysis Was Failed, Please check with Application!")
        set_request_status('Failed', analysis_id, e.msg)

    except Exception as e:
        sendEmailNotificatio(user_email_id, " Infinera Analysis ", " Your "+analysis_name+" Analysis Was Failed, Please check with Application!")
        print("SOME ERROR OCCURRED")
        print(150 * "*")
        print(str(e))
        set_request_status('Failed', analysis_id, 'Unknown Reason')
        print(150 * "*")

@celery.task
def bom_derive_table_creation(bom_file, sap_file, analysis_date, user_email_id, analysis_id, customer_name, prospect_id, replenish_time, analysis_name, is_mtbf):

    try:
        sendEmailNotificatio(user_email_id, " Infinera Analysis ", " Your " + analysis_name + " Analysis Submitted Successfully..")
        convert_headers_in_sap_file(sap_file)

        def set_request_status(status, analysis_id, msg):
            engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args)
            query = "update analysis_request set requestStatus='{0}',failure_reason='{2}' " \
                    "where analysis_request_id = {1}".format(status, analysis_id, msg)
            print(query)
            engine.execute(query)

        single_bom, high_spares, standard_cost, parts = get_bom_for_bom_record(bom_file, sap_file, analysis_date, analysis_id, prospect_id,
                                                                replenish_time, is_mtbf)

        update_prospect_step(prospect_id, 5, analysis_date)  # BOM calculation Status
        calculate_shared_depot(single_bom, high_spares, standard_cost, parts, analysis_date,
                               user_email_id, analysis_id, customer_name)

        update_prospect_step(prospect_id, 6, analysis_date)  # Summary Calculation  Status
        set_request_status('Completed', analysis_id, 'Success')
        sendEmailNotificatio(user_email_id, " Infinera Analysis ", "Your "+analysis_name+" Analysis Completed Successfully..")

    except CustomException as e:
        sendEmailNotificatio(user_email_id, " Infinera Analysis ", "Your "+analysis_name+" Analysis Was Failed, Please check with Application!")
        set_request_status('Failed', analysis_id, e.msg)

    except Exception as e:
        sendEmailNotificatio(user_email_id, " Infinera Analysis ", "Your "+analysis_name+" Analysis Was Failed, Please check with Application!")
        print("SOME ERROR OCCURRED")
        print(150 * "*")
        print(str(e))
        set_request_status('Failed', analysis_id, 'Unknown Reason')
        print(150 * "*")


@celery.task
def part_table_creation(part_file, extension, user_email_id):

    while check_analysis_task_status():
        import time
        print("The task part_table_creation is paused, as analysis request is running")
        time.sleep(60)

    print("The task part_table_creation started, as No analyis request is running")

    engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args)

    if extension.lower() == '.csv':
        part_df = pd.read_csv(part_file, error_bad_lines=False)

    elif extension.lower() == '.txt':
        part_df = pd.read_csv(part_file, sep='\t')

    elif extension.lower() == '.xls' or extension.lower() == '.xlsx':
        part_df = pd.read_excel(part_file)

    # Remove records having cost as NULL & part_name as NULL
    part_df.dropna(subset=['part_name', 'standard_cost'], inplace=True)

    # Remove duplicate part_name
    part_df.drop_duplicates(subset="part_name", keep="first", inplace=True)

    # Replace null in part_reliability_class to Others
    part_df['part_reliability_class'] = part_df['part_reliability_class'].fillna('Others')

    # Part table is without std_cost ,std_cost is seperate table
    part_table_column = ['material_number', 'part_name', 'part_reliability_class', 'spared_attribute'
                         , 'product_type', 'product_family', 'product_category', 'item_category', 'product_phase']

    # delete parts & append with new values
    query = "delete from parts"
    engine.execute(query)

    # Parts table populated
    to_sql_part_table(part_df[part_table_column])

    # To populate std_cost table,first get part_id with part_name
    df = pd.read_sql_table(table_name='parts', con=create_engine(Configuration.ECLIPSE_DATA_DB_URI, connect_args=Configuration.ssl_args))

    # keep only required column in dataframe
    df = df[['part_id', 'part_name']]

    # Merge with part_df to get part_id from part_name
    std_cost_df = pd.merge(part_df, df, on=['part_name'], how='left')
    std_cost_df = std_cost_df[['part_id', 'material_number', 'standard_cost']]
    std_cost_df['material_number'] = std_cost_df['material_number']

    # delete parts & append with new values
    query = "delete from `part_cost`"
    engine.execute(query)

    # std_cost table populated
    to_sql_std_cost_table(std_cost_df)
    sendEmailNotificatio(user_email_id, " Infinera Reference Data Upload  ",
                         " Your Request to upload Parts data finished ")


@celery.task
def depot_table_creation(depot_file, extension, user_email_id):

    while check_analysis_task_status():
        import time
        print("The task depot_table_creation is paused, as analysis request is running")
        time.sleep(60)

    print("The task depot_table_creation started, as No analyis request is running")

    engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args)

    if extension.lower() == '.csv':
        depot_df = pd.read_csv(depot_file, error_bad_lines=False)

    elif extension.lower() == '.txt':
        depot_df = pd.read_csv(depot_file, sep='\t')

    elif extension.lower() == '.xls' or extension.lower() == '.xlsx':
        depot_df = pd.read_excel(depot_file)

    # Remove duplicate part_name
    depot_df.drop_duplicates(subset="depot_name", keep="first", inplace=True)

    # delete depot  & append with new values
    query = "delete from depot"
    engine.execute(query)

    # depot table populated
    to_sql_depot_table(depot_df)
    sendEmailNotificatio(user_email_id, " Infinera Reference Data Upload  ",
                         " Your Request to upload Depot data finished ")


@celery.task
def node_table_creation(node_file, extension, user_email_id):

    while check_analysis_task_status():
        import time
        print("The task node_table_creation is paused, as analysis request is running")
        time.sleep(60)

    print("The task node_table_creation started, as No analyis request is running")

    engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args)

    if extension.lower() == '.csv':
        node_df = pd.read_csv(node_file, error_bad_lines=False)

    elif extension.lower() == '.txt':
        node_df = pd.read_csv(node_file, sep='\t')

    elif extension.lower() == '.xls' or extension.lower() == '.xlsx':
        node_df = pd.read_excel(node_file)

    # Remove duplicate from dataframe
    node_df.drop_duplicates(keep="first", inplace=True)

    node_df.rename(columns={
            'Node_Name': 'node_name',
            'End_Customer': 'end_customer_node_belongs',
            'Depot': 'node_depot_belongs'
        }, inplace=True
    )

    # delete node  & append with new values
    query = "delete from node"
    engine.execute(query)

    #depot table populated
    to_sql_node_table(node_df)

    # delete end_customer & append with new values
    query = "delete from end_customer"
    engine.execute(query)

    to_sql_end_customer_table(node_df)
    sendEmailNotificatio(user_email_id, " Infinera Reference Data Upload  ",
                         " Your Request to upload Node data finished ")


@celery.task
def high_spare_table_creation(high_spare_file, extension, user_email_id):

    while check_analysis_task_status():
        import time
        print("The task high_spare_table_creation is paused, as analysis request is running")
        time.sleep(60)

    print("The task high_spare_table_creation started, as No analyis request is running")

    engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args)

    if extension.lower() == '.csv':
        high_spare_df = pd.read_csv(high_spare_file, error_bad_lines=False)

    elif extension.lower() == '.txt':
        high_spare_df = pd.read_csv(high_spare_file, sep='\t')

    elif extension.lower() == '.xls' or extension.lower() == '.xlsx':
        high_spare_df = pd.read_excel(high_spare_file)

    # Remove duplicate from dataframe
    high_spare_df.drop_duplicates(keep="first", inplace=True)
    high_spare_df.rename(columns={'Classic_Part': 'part_name', 'Substitution_Part': 'high_spare_part_name'}, inplace=True)

    query = "delete from high_spare"
    engine.execute(query)

    # high_spare table populated
    to_sql_high_spare_table(high_spare_df)
    sendEmailNotificatio(user_email_id, " Infinera Reference Data Upload  ",
                         " Your Request to upload High Spare data finished ")



@celery.task
def misnomer_table_creation(misnomer_file, extension, user_email_id):

    while check_analysis_task_status():
        import time
        print("The task ratio_table_creation is paused, as analysis request is running")
        time.sleep(60)

    print("The task ratio_table_creation started, as No analyis request is running")

    engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args)

    if extension.lower() == '.csv':
        misnomer_df = pd.read_csv(misnomer_file, error_bad_lines=False)

    elif extension.lower() == '.txt':
        misnomer_df = pd.read_csv(misnomer_file, sep='\t')

    elif extension.lower() == '.xls' or extension.lower() == '.xlsx':
        misnomer_df = pd.read_excel(misnomer_file)

    # Remove duplicate from dataframe
    misnomer_df.drop_duplicates(keep="first", inplace=True)

    # delete high_spare  & append with new values
    query = "delete from `misnomer_part_conversion`"
    engine.execute(query)

    # high_spare table populated
    to_sql_misnomer_table(misnomer_df)
    sendEmailNotificatio(user_email_id, " Infinera Reference Data Upload  ",
                         " Your Request to upload Misnomer data finished ")


@celery.task
def ratio_table_creation(ratio_file, extension, analysis_type, user_email_id):

    while check_analysis_task_status():
        import time
        print("The task ratio_table_creation is paused, as analysis request is running")
        time.sleep(60)

    print("The task ratio_table_creation started, as No analyis request is running")

    engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args)

    if extension.lower() == '.csv':
        ratio_df = pd.read_csv(ratio_file, error_bad_lines=False)

    elif extension.lower() == '.txt':
        ratio_df = pd.read_csv(ratio_file, sep='\t')

    elif extension.lower() == '.xls' or extension.lower() == '.xlsx':
        ratio_df = pd.read_excel(ratio_file)

    # Reformat file to be in proper dataframe

    ratio_df.columns = ratio_df.iloc[np.where((ratio_df.isin(['Products'])) == True)[0]].values[0]
    ratio_df = ratio_df.iloc[(int(np.where((ratio_df.isin(['Products']) == True))[0])) + 1:]

    # Remove duplicate from dataframe
    ratio_df.drop_duplicates(keep="first", inplace=True)
    ratio_df['replenish_time'] = analysis_type

    # delete ratio  & append with new values
    query = "delete from reliability_class where replenish_time = '{0}'".format(analysis_type)
    print(query)
    engine.execute(query)

    # ratio table populated
    to_sql_reliability_class_table(ratio_df)
    sendEmailNotificatio(user_email_id, " Infinera Reference Data Upload  ",
                         " Your Request to upload Ratio of PON data finished ")


@celery.task
def end_customer_table_creation(end_customer_file, extension, user_email_id):

    while check_analysis_task_status():
        import time
        print("The task end_customer_table_creation is paused, as analysis request is running")
        time.sleep(60)

    print("The task end_customer_table_creation task started, as No analyis request is running")
    engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args)

    if extension.lower() == '.csv':
        end_customer_df = pd.read_csv(end_customer_file, error_bad_lines=False)

    elif extension.lower() == '.txt':
        end_customer_df = pd.read_csv(end_customer_file, sep='\t')

    elif extension.lower() == '.xls' or extension.lower() == '.xlsx':
        end_customer_df = pd.read_excel(end_customer_file)

    # Remove duplicate cust_name
    end_customer_df.drop_duplicates(subset="Customer_Name", keep="first", inplace=True)

    # delete end_customer  & append with new values
    query = "delete from end_customer"
    engine.execute(query)

    # end_customer table populated
    to_sql_end_customer(end_customer_df)
    sendEmailNotificatio(user_email_id, " Infinera Reference Data Upload  ", " Your Request to upload Customer data finished ")


@celery.task
def lab_table_creation(lab_file, extension, user_email_id):

    while check_analysis_task_status():
        import time
        print("The task lab_table_creation is paused, as analysis request is running")
        time.sleep(60)

    print("The task lab_table_creation task started, as No analyis request is running")
    engine = create_engine(Configuration.INFINERA_DB_URL, connect_args=Configuration.ssl_args)

    if extension.lower() == '.csv':
        lab_df = pd.read_csv(lab_file, error_bad_lines=False)

    elif extension.lower() == '.txt':
        lab_df = pd.read_csv(lab_file, sep='\t')

    elif extension.lower() == '.xls' or extension.lower() == '.xlsx':
        lab_df = pd.read_excel(lab_file)

    # Remove duplicate cust_name
    lab_df.drop_duplicates(subset="Lab System Name", keep="first", inplace=True)

    # delete end_customer  & append with new values
    query = "delete from lab_systems"
    engine.execute(query)

    # lab_systems table populated
    to_sql_lab_systems(lab_df)
    sendEmailNotificatio(user_email_id, " Infinera Reference Data Upload  ", " Your Request to upload Labs data finished ")















