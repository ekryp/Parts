import json
import os
import pandas as pd
from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy import exc
from shutil import copy
import glob
import time
import smtplib
from email.mime.text import MIMEText

from app import app
from app import Configuration

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import math
import sys
import os
import timeit

engine = create_engine(Configuration.INFINERA_DB_URL)
connection = Configuration.INFINERA_DB_URL


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

def read_data(sql, con):
    connection = create_engine(con)
    return pd.read_sql(sql, con=connection)


def clean_pon_names(input_db):
    input_db['Product Ordering Name'] = input_db['Product Ordering Name'].str.replace('/[^a-zA-Z0-9-*.]/','').str.strip()
    input_db['InstalledEqpt'] = input_db['InstalledEqpt'].str.replace('/[^a-zA-Z0-9-*.]/', '').str.strip()
    input_db['Part#'] = input_db['Part#'].str.replace('/[^a-zA-Z0-9-*.]/', '').str.strip()
    return input_db


def misnomer_conversion(input_db, misnomer_pons):
    input_with_no_misnomer_pon = pd.DataFrame()
    input_with_no_misnomer_pon = pd.merge(input_db, misnomer_pons, left_on='part_ordering_number', right_on='misnomer_pon_name', how='left')


    input_with_no_misnomer_pon.loc[(input_with_no_misnomer_pon['part_ordering_number'] == input_with_no_misnomer_pon['misnomer_pon_name']), 'part_ordering_number'] = input_with_no_misnomer_pon['part_ordering_number']
    input_with_no_misnomer_pon = input_with_no_misnomer_pon.drop(['misnomer_pon_name'], 1)

    input_with_no_misnomer_pon = pd.merge(input_with_no_misnomer_pon, misnomer_pons, left_on='installed_eqpt',right_on='misnomer_pon_name', how='left')

    input_with_no_misnomer_pon.loc[(input_with_no_misnomer_pon['installed_eqpt'] == input_with_no_misnomer_pon['misnomer_pon_name']), 'installed_eqpt'] = input_with_no_misnomer_pon['part_ordering_number']
    input_with_no_misnomer_pon = input_with_no_misnomer_pon.drop(['misnomer_pon_name'], 1)

    print(misnomer_pons.columns)
    input_with_no_misnomer_pon = pd.merge(input_with_no_misnomer_pon, misnomer_pons, left_on='part', right_on= 'misnomer_pon_name', how='left')
    input_with_no_misnomer_pon.loc[(input_with_no_misnomer_pon['part'] == input_with_no_misnomer_pon['misnomer_pon_name']), 'part'] = input_with_no_misnomer_pon['part_ordering_number']

    input_with_no_misnomer_pon = input_with_no_misnomer_pon.drop(['misnomer_pon_name'], 1)

    return input_with_no_misnomer_pon


def check_in_std_cst(input_DB_merge_PON_Misnomer, Standard_Cost):
    for i in range(len(input_DB_merge_PON_Misnomer)):
        if (str(input_DB_merge_PON_Misnomer['part_ordering_number'][i]) in ("CHASSIS")):
            input_DB_merge_PON_Misnomer['part_ordering_number'][i] = input_DB_merge_PON_Misnomer['installed_eqpt'][i]
        else:
            if (isinarray(input_DB_merge_PON_Misnomer['part_ordering_number'][i], Standard_Cost) == True):
                input_DB_merge_PON_Misnomer['part_ordering_number'][i] = \
                input_DB_merge_PON_Misnomer['part_ordering_number'][i]

            elif (isinarray(input_DB_merge_PON_Misnomer['installed_eqpt'][i], Standard_Cost) == True):
                input_DB_merge_PON_Misnomer['part_ordering_number'][i] = input_DB_merge_PON_Misnomer['installed_eqpt'][
                    i]

            elif (isinarray(input_DB_merge_PON_Misnomer['part'][i], Standard_Cost) == True):
                input_DB_merge_PON_Misnomer['part_ordering_number'][i] = input_DB_merge_PON_Misnomer['part'][i]
    return input_DB_merge_PON_Misnomer


def isinarray(Input_Data, Standard_cost):
    for j in range(len(Standard_cost['part_name'])):
        if Input_Data == Standard_cost['part_name'][j]:
            return True
    return False


def to_sql_customer_dna_record(table_name, df):
    engine = Configuration.ECLIPSE_DATA_DB_URI
    df['cust_id'] = 7
    df['end_customer_id'] = 1
    df.rename(columns={
        '#Type': 'type',
        'Node ID': 'node_id',
        'AID': 'aid',
        'InstalledEqpt': 'installed_eqpt',
        'Product Ordering Name': 'part_ordering_number',
        'Part#': 'part',
        'Serial#': 'serial',
        'Source': 'source_part_data',
        'Node Name': 'node_name'
    }, inplace=True
    )
    keep_col = ['cust_id', 'type', 'node_id', 'installed_eqpt', 'part_ordering_number', 'part', 'serial',
                'source_part_data', 'aid', 'end_customer_id']
    df = df[keep_col]
    df.to_sql(name=table_name, con=engine, index=False, if_exists='append')
    print("Loaded Data into table : {0}".format(table_name))


def to_sql_summarytable(table_name, df):
    engine = Configuration.ECLIPSE_DATA_DB_URI
    df['cust_id'] = 7
    df['summary_table'] = 1
    df.rename(columns={
        'material_number_x' : 'material_number',
        'standard_cost_x' : 'standard_cost'
    }, inplace=True
    )
    keep_col = ['cust_id', 'summary_table', 'PON', 'material_number', 'Qty','standard_cost','gross table count','extd std cost','High Spares?','net depot count','net extd std cost']
    df = df[keep_col]
    df.to_sql(name=table_name, con=engine, index=False, if_exists='append')
    print("Loaded Data into table : {0}".format(table_name))

def validate_pon(pon):
    invalid_list = ["", "none", "n/a", "null", "chassis", "unknown", "@", ".."]
    for col_name in ['part_ordering_number', 'installed_eqpt']:
        pon.loc[pon[col_name].isin(invalid_list), 'Is Valid' + ' ' + str(col_name)] = False
    return pon


def validate_depot(pon):
    invalid_list = ["not 4hr", "not supported"]
    for col_name in ['node_depot_belongs']:
        pon.loc[pon[col_name].str.lower().isin(invalid_list), 'Is Valid' + ' ' + str(col_name)] = False
    return pon

def find_spare_bin(row):
    bins = [0] + list(row[spare_cols])
    # Check for empyt count, if there is no calss family for PON
    # Then make required spared = 1, the logic is make the first column == FRU count
    # the return spare would be 1
    bins = [row['count'] if math.isnan(x) else x for x in bins]
    return np.digitize(row['count'], bins, right=True)

# this function is in place
'''
Check if current depot is hub or a depot
if it is not a hub, check if PONs are in Chassis array
if PONs are in chassis array make gross depot count to 0
'''
def adjust_chassis():
    ChassisArray = ["DTC-ANSI-B=", "DTC-ETSI-B=", "OTC-ANSI-A=", "OTC-ETSI-A=", "XTC-2", "XTC-4", "XTC-10",
                         "XTC-2E", "MTC-9-B", "MTC-6", "MPC-6", "MTC-9", "MTC-ANSI="]

    hubs = pd.merge(depot, shared_depot_sub_pon, on = 'Storage Location = Depot Name', how= 'inner')
    print(hubs)
    hubs = hubs[['Storage Location = Depot Name']]
    #check if current depot is hub
    if (hubs['Storage Location = Depot Name'] == 0):
        for i in gross_bom_depot_get_std_Cost['part_name']:
            if gross_bom_depot_get_std_Cost[i].isin(ChassisArray) == True:
                print('some chaiss depot avilable')
                gross_bom_depot_get_std_Cost['gross table count'][i] = 0

        print( gross_bom_depot_get_std_Cost['gross table count'][i] )

@celery.task
def derive_table_creation(dna_file, sap_file, data_path):
    print(dna_file, sap_file)
    get_misnomer_sql = "SELECT mp.misnomer_pon_name, pt.part_name FROM infinera.`Misnomer PON Conversion` mp, infinera.`parts` pt where mp.correct_part_id = pt.part_id ;"
    get_standard_cost = "SELECT pt.part_name, pt.material_number FROM infinera.`part cost ID` pid right join infinera.parts pt on pt.part_id =pid.part_id where part_name != 'null'"
    get_node = "SELECT * FROM infinera.node where end_customer_node_belongs = 'Bestel' ;"
    input_db_sql = "select * FROM infinera.customer_dna_record;"
    input_db = pd.read_csv(dna_file, sep='\t')
    input_db = clean_pon_names(input_db)
    print("Dumping to table customer_dna_record")
    to_sql_customer_dna_record('customer_dna_record', input_db)
    print("Dumping Complete to table customer_dna_record")
    input_db = read_data(input_db_sql, connection)

    # dump input_db as it is in table INPUT_DB
    misnomer_pons = read_data(get_misnomer_sql, connection)
    standard_cost = read_data(get_standard_cost, connection)
    node = read_data(get_node, connection)

    unspared_sql = "SELECT part_name FROM infinera.parts where spared_attribute = 0;"
    unspared_pons = read_data(unspared_sql, connection)

    high_spare_sql = "SELECT pt.part_name, given_spare_part_id, high_spare_part_id FROM infinera.high_spare, infinera.parts pt where given_spare_part_id = pt.part_id;"
    highspares = read_data(high_spare_sql, connection)

    get_ratio_to_pon_sql = "SELECT * FROM infinera.failure_information where replenish_timetable_id = 1;"
    get_ratio_to_pon = read_data(get_ratio_to_pon_sql, connection)

    get_parts_sql = 'SELECT * FROM infinera.parts;'
    parts = read_data(get_parts_sql, connection)

    get_parts_cost_sql = "SELECT * FROM infinera.`part cost ID` pid, infinera.parts pt where  pt.material_number = pid.material_number;"
    parts_cost = read_data(get_parts_cost_sql, connection)

    get_high_spares = "SELECT pt.part_name, given_spare_part_id, high_spare_part_id FROM infinera.high_spare, infinera.parts pt where given_spare_part_id = pt.part_id;"
    high_spares = read_data(get_high_spares, connection)

    get_depot_sql = "SELECT depot_name, depot_id FROM infinera.depot;"
    depot = read_data(get_depot_sql, connection)

    sap_inventory = sap_inventory_data = pd.read_excel(sap_file, sheet_name='Sheet1')
    print('data fetch complete')

    # clean PONs, part# and installed equipments


    # PON with no misnomers
    input_with_no_misnomer_pon = misnomer_conversion(input_db, misnomer_pons)

    print('Checking PON, part# in std cost...')
    input_with_no_misnomer_pon = check_in_std_cst(input_with_no_misnomer_pon, standard_cost)

    # Assign PON tp Installed quipments to remove any ambiguity
    input_with_no_misnomer_pon['installed_eqpt'] = input_with_no_misnomer_pon['part_ordering_number']

    ##  We are merging this to get the depot name and locatopn
    input_with_no_misnomer_pon = pd.merge(input_with_no_misnomer_pon, node, left_on='node_name', right_on='node_name',
                                          how='left')
    input_with_no_misnomer_pon = input_with_no_misnomer_pon[
        (input_with_no_misnomer_pon['part_ordering_number'] != 'null')]

    input_with_no_misnomer_pon = validate_pon(input_with_no_misnomer_pon)
    input_with_no_misnomer_pon = validate_depot(input_with_no_misnomer_pon)

    input_DB_merge_PON_Misnomer_valid_PON = input_with_no_misnomer_pon[
        (input_with_no_misnomer_pon['Is Valid Product Ordering Name'] != False) & (
            input_with_no_misnomer_pon['Is Valid node_depot_belongs'] != False)]

    input_DB_merge_PON_Misnomer_valid_PON = pd.merge(input_DB_merge_PON_Misnomer_valid_PON, standard_cost,
                                                     left_on=['part_ordering_number'], right_on=['part_name'],
                                                     how='left')
    input_DB_merge_PON_Misnomer_valid_PON.loc[(input_DB_merge_PON_Misnomer_valid_PON['part_ordering_number'] ==
                                               input_DB_merge_PON_Misnomer_valid_PON[
                                                   'part_ordering_number']), 'Std_row'] = 99

    input_DB_merge_PON_Misnomer_valid_PON = pd.merge(input_DB_merge_PON_Misnomer_valid_PON, unspared_pons,
                                                     left_on=['part_ordering_number'], right_on=['part_name'],
                                                     how='left')
    input_DB_merge_PON_Misnomer_valid_PON.loc[(input_DB_merge_PON_Misnomer_valid_PON['part_ordering_number'] ==
                                               input_DB_merge_PON_Misnomer_valid_PON[
                                                   'part_ordering_number_x']), 'Unspared'] = 99

    input_DB_merge_PON_Misnomer_valid_PON_add_missing = input_DB_merge_PON_Misnomer_valid_PON[
        input_DB_merge_PON_Misnomer_valid_PON['Unspared'] == 0]

    # Have to add check for missing PON in SAP
    # Missing values in high spares

    Missing_PONs = input_DB_merge_PON_Misnomer_valid_PON[(input_DB_merge_PON_Misnomer_valid_PON['Unspared'] != 99) &
                                                         (input_DB_merge_PON_Misnomer_valid_PON['Std_row'] != 99)]
    Missing_PONs_values = Missing_PONs[Missing_PONs['Is Valid Product Ordering Name'] == False]
    Missing_PONs_values.loc[
        (Missing_PONs_values['part_name'] == Missing_PONs_values['part_name_x']), 'part_name'] = \
        Missing_PONs_values['part_name']

    Invalid_and_missing_values = input_DB_merge_PON_Misnomer_valid_PON[
        (input_DB_merge_PON_Misnomer_valid_PON['Is Valid Product Ordering Name'] == False) &
        (input_DB_merge_PON_Misnomer_valid_PON['node_depot_belongs'] == "" "")]

    Valid_values = input_DB_merge_PON_Misnomer_valid_PON[
        (input_DB_merge_PON_Misnomer_valid_PON['Is Valid Product Ordering Name'] != False) &
        (input_DB_merge_PON_Misnomer_valid_PON['Is Valid InstalledEqpt'] != False) &
        (input_DB_merge_PON_Misnomer_valid_PON['Is Valid node_depot_belongs'] != False)]
    Missing_Node_values = input_DB_merge_PON_Misnomer_valid_PON[
        input_DB_merge_PON_Misnomer_valid_PON['node_name'] == '']
    Missing_Node_values = pd.merge(Valid_values, Missing_Node_values, left_on=['node_name'], right_on=['node_name'],
                                   how='inner')
    try:
        Missing_Node_values.loc[(Missing_Node_values['node_name'] == Valid_values['node_name']), 'Missing Node Name'] = \
            Missing_Node_values['node_name']
    except:
        pass

    # calculating BOM
    print('calculating BOM')

    DNA_BOM = Valid_values.pivot_table(columns='node_depot_belongs', index=Valid_values['part_ordering_number'],
                                       values='part_ordering_number', aggfunc="count", fill_value=0)
    DNA_BOM['HNAD'] = 1
    DNA_BOM['Qty'] = DNA_BOM.sum(axis=1)
    DNA_BOM = DNA_BOM.reindex(sorted(DNA_BOM.columns), axis=1)

    Get_Fru = pd.DataFrame(
        Valid_values.groupby(['part_ordering_number', 'node_depot_belongs', 'Source'])['node_depot_belongs'].count())
    print('BOM calculation complete')
    Get_Fru.to_csv(os.path.join(data_path, Configuration.fruc_file_location), index=True)
    Get_Fru = pd.read_csv(os.path.join(data_path, Configuration.fruc_file_location))
    Get_Fru = Get_Fru.rename(columns={'node_depot_belongs.1': 'count'})
    Get_Fru_count = pd.merge(Get_Fru, parts, left_on='part_ordering_number', right_on='part_name', how='left')
    Get_Fru_count = Get_Fru_count[['part_name', 'node_depot_belongs', 'count', 'part_reliability_class']]
    Get_Fru_count.groupby(['part_name', 'node_depot_belongs'])['count'].last().unstack(fill_value=0).stack().to_csv(
        os.path.join(data_path, Configuration.bom_table), header=True)
    get_bom_for_table = pd.read_csv(os.path.join(data_path, Configuration.bom_table))
    get_bom_for_table = get_bom_for_table.rename(columns={'0': 'PON Quanity'})
    get_bom_for_table = pd.merge(get_bom_for_table, parts, left_on='part_name', right_on='part_name',
                                 how='inner').merge(depot, left_on='node_depot_belongs', right_on='depot_name',
                                                    how='inner')
    get_bom_for_table = get_bom_for_table[
        ['part_id', 'cust_id', 'node_depot_belongs', 'PON Quanity', 'depot_id', 'part_name']]
    # get_bom_for_table.sort_values(by = ['part_name','node_depot_belongs']).to_csv(Configuration.bom_table)

    bom_to_table_to_db = get_bom_for_table[['part_id', 'cust_id', 'PON Quanity', 'depot_id']]
    bom_to_table_to_db = bom_to_table_to_db.rename(columns={'PON Quanity': 'pon_quantity'})
    bom_to_table_to_db['end_cust_id'] = pd.read_sql(
        "SELECT end_cust_id FROM infinera.end_customer where end_cust_name = 'Bestel'; ", connection)
    bom_to_table_to_db.to_sql(name='bom_calculated', con=engine, index=False, if_exists='append', chunksize=1000)

    spare_cols = [str(x + 1) for x in range(10)]

    print('MTBF calculation done...')

    Get_MTBF_BOM = pd.merge(Get_Fru_count, get_ratio_to_pon, left_on='part_reliability_class',
                            right_on='product_family', how='left')
    Get_MTBF_BOM['result'] = Get_MTBF_BOM.apply(find_spare_bin, axis=1)
    Get_MTBF_BOM_calc = Get_MTBF_BOM[['part_name', 'node_depot_belongs', 'result']]
    Get_MTBF_BOM_calc_table = Get_MTBF_BOM_calc.pivot(index='part_name', columns='node_depot_belongs',
                                                      values='result')
    Get_MTBF_BOM_calc_table['HNAD'] = 1
    Get_MTBF_BOM_calc_table = Get_MTBF_BOM_calc_table.reindex(sorted(DNA_BOM.columns), axis=1)

    Get_MTBF_BOM_calc.groupby(['part_name', 'node_depot_belongs'])['result'].last().unstack(
        fill_value=0).stack().to_csv(os.path.join(data_path, Configuration.mtbf_bom_table), header=True)
    mtbf_bom_to_table = pd.read_csv(os.path.join(data_path, Configuration.mtbf_bom_table))
    mtbf_bom_to_table = mtbf_bom_to_table.rename(columns={'0': 'PON Quanity'})
    mtbf_bom_to_table = pd.merge(mtbf_bom_to_table, parts, left_on='part_name', right_on='part_name',
                                 how='inner').merge(depot, left_on='node_depot_belongs', right_on='depot_name',
                                                    how='inner')
    mtbf_bom_to_table = mtbf_bom_to_table[
        ['part_id', 'cust_id', 'node_depot_belongs', 'PON Quanity', 'depot_id', 'part_name']]
    mtbf_bom_to_table = mtbf_bom_to_table.rename(columns={'PON Quanity': 'pon_quantity'})
    mbf_bom_to_table_sql = mtbf_bom_to_table[['part_id', 'cust_id', 'pon_quantity', 'depot_id']]
    mbf_bom_to_table_sql['end_cust_id'] = pd.read_sql(
        "SELECT end_cust_id FROM infinera.end_customer where end_cust_name = 'Bestel'; ", connection)
    mbf_bom_to_table_sql.to_sql(name='mtbf_bom_calculated', con=engine, index=False, if_exists='append', chunksize=1000)

    DNA_BOM.to_csv(os.path.join(data_path, Configuration.DNA_BOM), header=True)
    Get_MTBF_BOM_calc_table.to_csv(os.path.join(data_path, Configuration.MTBF_BOM), header=True)

    # get unique PONs, then check if PONs are present in Unspared PON
    # get unsparedPONs and select only those PONs that are not in Unspared
    Uniques_PONs = Get_MTBF_BOM_calc['part_name'].unique()
    spared_pons = unspared_pons[(unspared_pons['part_name'].isin(Uniques_PONs))]
    spared_pon_for_material = Valid_values[~(Valid_values['part_name'].isin(spared_pons['part_name']))]

    Summary = pd.DataFrame(columns=['Item Number', 'Material', 'Quantity', 'Std cost'])
    Summary['Item Number'] = (spared_pon_for_material['part_name_x'].unique())
    Summary['Material'] = (spared_pon_for_material['material_number'].unique())
    get_Route_qty = pd.DataFrame(spared_pon_for_material['part_name_x'].unique())
    get_Route_qty['PON'] = get_Route_qty
    Get_rout_value = pd.merge(get_Route_qty, DNA_BOM, left_on='PON', right_on='part_name', how='inner')
    Get_rout_value = Get_rout_value[['PON', 'Qty']]
    Summary_table = pd.merge(Get_rout_value, parts_cost, left_on='PON', right_on='part_name', how='inner').merge(
        standard_cost, left_on='part_name', right_on='part_name', how='inner')

    Summary_table = Summary_table[['PON', 'material_number_x', 'Qty', 'standard_cost']]
    Summary_table = Summary_table.sort_values(by='PON')
    Summary_table.loc[Summary_table['PON'].isin(high_spares['part_name']), 'High Spares?'] = 'True'
    Summary_table['High Spares?'] = Summary_table['High Spares?'].fillna(value=0)
    Summary_table = Summary_table.loc[:, ~Summary_table.columns.duplicated()]
    Summary_table = Summary_table.rename(columns={'material_number_x': 'material_number'})
    Summary_table.to_csv(os.path.join(data_path, Configuration.summary_output), header=True)

    submatrix = pd.merge(parts, high_spares, on='part_name', how='inner')
    submatrix_new = pd.merge(submatrix, parts, left_on='high_spare_part_id', right_on='part_id')
    submatrix_new = submatrix_new[['part_id_x', 'part_name_x', 'part_name_y', 'part_id_y']]

    get_Shared_Depot = sap_inventory_data[
        sap_inventory_data['Material Description = Part Name'].isin(Summary_table['PON']) & (
        sap_inventory_data['Storage Location = Depot Name'].isin(Get_MTBF_BOM_calc['node_depot_belongs']))]

    shared_depot = pd.merge(Summary_table, get_Shared_Depot, left_on='PON', right_on='Material Description = Part Name',
                            how='left')
    shared_depot.loc[shared_depot['Storage Location = Depot Name'].isnull(), 'Storage Location = Depot Name'] = \
    shared_depot['Storage Location = Depot Name'][1]
    shared_depot.loc[shared_depot['Reorder Point'].isnull(), 'Reorder Point'] = 0
    shared_depot.loc[shared_depot['Total Stock'].isnull(), 'Total Stock'] = 0

    ##if total stock is not selected then select roerder point
    get_Shared_Depot_table = shared_depot.pivot_table(index='PON', columns='Storage Location = Depot Name',
                                                      values='Reorder Point')
    get_Shared_Depot_table.to_csv(os.path.join(data_path, Configuration.shared_depot_file_location), header=True)
    # Get_MTBF_BOM_calc.pivot(index ='part_name', columns = 'Node_Depot_Belongs', values = 'result')

    # if use full stock is null
    shared_depot.groupby(['PON', 'Storage Location = Depot Name'])['Reorder Point'].last().unstack(
        fill_value=0).stack().to_csv(os.path.join(data_path, Configuration.shared_depot_file_location), header=True)
    # if use full is not unchecked
    # shared_depot.groupby(['PON','Storage Location = Depot Name'])['Total Stock'].last().unstack(fill_value=0).stack().to_csv('Data/sharedfiledepot.csv', header = True)

    mtbf_bom_to_table.groupby(['part_name', 'node_depot_belongs'])['node_depot_belongs'].count().unstack(
        fill_value=0).stack().to_csv(os.path.join(data_path, Configuration.mtbf_bom_table), header=True)
    get_bom_for_table.groupby(['part_name', 'node_depot_belongs'])['node_depot_belongs'].count().unstack(
        fill_value=0).stack().to_csv(os.path.join(data_path, Configuration.bom_table), header=True)

    shared_Depot_file = pd.read_csv(os.path.join(data_path, Configuration.shared_depot_file_location))

    gross_depot_bom = pd.read_csv(os.path.join(data_path, Configuration.bom_table))
    gross_depot_mtbf_bom = pd.read_csv(os.path.join(data_path, Configuration.mtbf_bom_table))

    get_bom_for_table.loc[get_bom_for_table['PON Quanity'] > 0, 'gross table count'] = 1
    get_bom_for_table.replace(np.nan, 0)
    mtbf_bom_to_table.loc[mtbf_bom_to_table['pon_quantity'] > 0, 'gross table count'] = 1
    mtbf_bom_to_table.replace(np.nan, 0)

    get_bom_for_table.groupby(['part_name'])['gross table count'].sum().to_csv(
        os.path.join(data_path, Configuration.gross_quantity_bom_depot_file_location), header=True)
    mtbf_bom_to_table.groupby(['part_name'])['gross table count'].sum().to_csv(
        os.path.join(data_path, Configuration.gross_quantity_mtbf_bom_depot_file_location, header=True))

    gross_depot_quantity_bom = pd.read_csv(os.path.join(data_path, Configuration.gross_quantity_bom_depot_file_location))
    gross_depot_quantity_mtbf_bom = pd.read_csv(os.path.join(data_path, Configuration.gross_quantity_mtbf_bom_depot_file_location))

    gross_depot_quantity_bom['gross table count'] = gross_depot_quantity_bom['gross table count'] + 1
    gross_depot_quantity_mtbf_bom['gross table count'] = gross_depot_quantity_mtbf_bom['gross table count'] + 1

    gross_bom_depot_get_std_Cost = pd.merge(gross_depot_quantity_bom, parts_cost, left_on='part_name',
                                            right_on='part_name', how='left')
    gross_mtbf_bom_depot_get_std_Cost = pd.merge(gross_depot_quantity_mtbf_bom, parts_cost, left_on='part_name',
                                                 right_on='part_name', how='left')

    gross_bom_depot_get_std_Cost = gross_bom_depot_get_std_Cost[['part_name', 'standard_cost', 'gross table count']]
    gross_mtbf_bom_depot_get_std_Cost = gross_mtbf_bom_depot_get_std_Cost[
        ['part_name', 'standard_cost', 'gross table count']]
    gross_bom_depot_get_std_Cost = gross_bom_depot_get_std_Cost[
        gross_bom_depot_get_std_Cost['part_name'].isin(Summary_table['PON'])]
    gross_mtbf_bom_depot_get_std_Cost = gross_mtbf_bom_depot_get_std_Cost[
        gross_mtbf_bom_depot_get_std_Cost['part_name'].isin(Summary_table['PON'])]
    gross_bom_depot_get_std_Cost['extd std cost'] = gross_bom_depot_get_std_Cost['gross table count'] * \
                                                    gross_bom_depot_get_std_Cost['standard_cost']
    gross_mtbf_bom_depot_get_std_Cost['extd std cost'] = gross_mtbf_bom_depot_get_std_Cost['gross table count'] * \
                                                         gross_mtbf_bom_depot_get_std_Cost['standard_cost']

    shared_x = shared_depot.loc[shared_depot['PON'].isin(submatrix_new['part_name_y'])]
    shared_x = shared_depot.loc[shared_depot['PON'].isin(submatrix_new['part_name_x'])]
    shared_x = shared_x[['Reorder Point', 'PON', 'Storage Location = Depot Name']]

    shared_depot_sub_pon = pd.merge(shared_Depot_file, submatrix_new, left_on='PON', right_on='part_name_x', how='left')
    shared_depot_sub_pon = pd.merge(shared_depot_sub_pon, shared_depot_sub_pon,
                                    left_on=['part_name_y', 'Storage Location = Depot Name'],
                                    right_on=['PON', 'Storage Location = Depot Name'], how='left')
    shared_depot_sub_pon = shared_depot_sub_pon[
        ['PON_x', 'Storage Location = Depot Name', '0_x', 'part_name_x_x', 'part_name_y_x', 'part_id_y_x', 'PON_y',
         '0_y']]
    shared_depot_sub_pon.loc[shared_depot_sub_pon['PON_x'] == shared_depot_sub_pon['part_name_x_x'], '0_x'] = \
    shared_depot_sub_pon['0_y']
    shared_depot_sub_pon = shared_depot_sub_pon[['PON_x', 'Storage Location = Depot Name', '0_x']]

    # if BOM
    net = pd.merge(shared_depot_sub_pon, get_bom_for_table, left_on=['PON_x', 'Storage Location = Depot Name'],
                   right_on=['part_name', 'node_depot_belongs'], how='left')
    # else
    # net = pd.merge(shared_depot_sub_pon, mtbf_bom_to_table, left_on = ['PON_x','Storage Location = Depot Name'], right_on = ['part_name','node_depot_belongs'], how = 'left')

    net.loc[net['PON Quanity'] > 0, 'gross table count'] = 1
    net['gross table count'] = net['gross table count'].replace(np.nan, 0)
    net['net depot count'] = np.where(net['gross table count'] - net['0_x'] > 0, net['gross table count'] - net['0_x'],
                                      0)

    net.groupby(['part_name'])['net depot count'].sum().to_csv(os.path.join(data_path, Configuration.net_depot, header=True))
    net_table = pd.read_csv(os.path.join(data_path, Configuration.net_depot))
    # net_table['net extd std cost'] = net_table['net depot count']*Summary_table['standard_cost']

    output = pd.merge(Summary_table, gross_mtbf_bom_depot_get_std_Cost, left_on='PON', right_on='part_name',
                      how='inner')
    output = pd.merge(output, net_table, left_on='PON', right_on='part_name')
    output['net extd std cost'] = output['net depot count'] * output['standard_cost_x']
    output = output.drop_duplicates(subset='PON')
    output = output[
        ['PON', 'material_number', 'Qty', 'standard_cost_x', 'gross table count', 'extd std cost', 'High Spares?',
         'net depot count', 'net extd std cost']]
    output.to_csv(os.path.join(data_path, Configuration.final_output))

    to_sql_summarytable('summary_output', output)






