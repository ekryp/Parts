import pandas as pd
from app import Configuration
from sqlalchemy import create_engine

engine = create_engine(Configuration.ECLIPSE_DATA_DB_URI)


def read_data(sql, con):
    connection = create_engine(con)
    return pd.read_sql(sql, con=connection)


def clean_pon_names(input_db):
    try:
        input_db['Product Ordering Name'] = input_db['Product Ordering Name'].str.replace('/[^a-zA-Z0-9-*.]/',
                                                                                          '').str.strip()
        input_db['InstalledEqpt'] = input_db['InstalledEqpt'].str.replace('/[^a-zA-Z0-9-*.]/', '').str.strip()
        input_db['Part#'] = input_db['Part#'].str.replace('/[^a-zA-Z0-9-*.]/', '').str.strip()
    except:
        input_db['Product Ordering Name'] = (input_db['Product Ordering Name'].astype(str)).str.replace('/[^a-zA-Z0-9-*.]/',
                                                                                          '').str.strip()
        input_db['InstalledEqpt'] = (input_db['InstalledEqpt'].astype(str)).str.replace('/[^a-zA-Z0-9-*.]/', '').str.strip()
        input_db['Part#'] = (input_db['Part#'].astype(str)).str.replace('/[^a-zA-Z0-9-*.]/', '').str.strip()
    return input_db


def misnomer_conversion(input_db, misnomer_pons):
    input_with_no_misnomer_pon = pd.DataFrame()
    input_with_no_misnomer_pon = pd.merge(input_db, misnomer_pons, left_on='Product Ordering Name',
                                          right_on='misnomer_pon_name', how='left')
    input_with_no_misnomer_pon.loc[(input_with_no_misnomer_pon['Product Ordering Name'] == input_with_no_misnomer_pon[
        'misnomer_pon_name']), 'Product Ordering Name'] = input_with_no_misnomer_pon['part_name']
    input_with_no_misnomer_pon = input_with_no_misnomer_pon.drop(['misnomer_pon_name', 'part_name'], 1)

    input_with_no_misnomer_pon = pd.merge(input_with_no_misnomer_pon, misnomer_pons, left_on='InstalledEqpt',
                                          right_on='misnomer_pon_name', how='left')
    input_with_no_misnomer_pon.loc[(input_with_no_misnomer_pon['InstalledEqpt'] == input_with_no_misnomer_pon[
        'misnomer_pon_name']), 'InstalledEqpt'] = input_with_no_misnomer_pon['part_name']
    input_with_no_misnomer_pon = input_with_no_misnomer_pon.drop(['misnomer_pon_name', 'part_name'], 1)

    input_with_no_misnomer_pon = pd.merge(input_with_no_misnomer_pon, misnomer_pons, left_on='Part#',
                                          right_on='misnomer_pon_name', how='left')
    input_with_no_misnomer_pon.loc[
        (input_with_no_misnomer_pon['Part#'] == input_with_no_misnomer_pon['misnomer_pon_name']), 'Part#'] = \
    input_with_no_misnomer_pon['part_name']
    input_with_no_misnomer_pon = input_with_no_misnomer_pon.drop(['misnomer_pon_name', 'part_name'], 1)

    return input_with_no_misnomer_pon


def check_in_std_cst(input_DB_merge_PON_Misnomer, Standard_Cost):
    for i in range(len(input_DB_merge_PON_Misnomer)):
        if (str(input_DB_merge_PON_Misnomer['Product Ordering Name'][i]) in ("CHASSIS")):
            input_DB_merge_PON_Misnomer['Product Ordering Name'][i] = input_DB_merge_PON_Misnomer['InstalledEqpt'][i]
        else:
            if (isinarray(input_DB_merge_PON_Misnomer['Product Ordering Name'][i], Standard_Cost) == True):
                input_DB_merge_PON_Misnomer['Product Ordering Name'][i] = \
                input_DB_merge_PON_Misnomer['Product Ordering Name'][i]

            elif (isinarray(input_DB_merge_PON_Misnomer['InstalledEqpt'][i], Standard_Cost) == True):
                input_DB_merge_PON_Misnomer['Product Ordering Name'][i] = input_DB_merge_PON_Misnomer['InstalledEqpt'][
                    i]

            elif (isinarray(input_DB_merge_PON_Misnomer['Part#'][i], Standard_Cost) == True):
                input_DB_merge_PON_Misnomer['Product Ordering Name'][i] = input_DB_merge_PON_Misnomer['Part#'][i]
    return input_DB_merge_PON_Misnomer


def isinarray(Input_Data, Standard_cost):
    for j in range(len(Standard_cost['part_name'])):
        if Input_Data == Standard_cost['part_name'][j]:
            return True
    return False


def to_sql_customer_dna_record(table_name, df, analysis_date, analysis_id):
    # Analysis datetime will come from frontend to bind with analysis request id
    # For now it would be a current time
    # analysis_date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    # df['analysis_request_time'] = analysis_date
    engine = Configuration.ECLIPSE_DATA_DB_URI
    # Hardcoded to 7  infinera
    #df['cust_id'] = 7
    df.loc[:, 'analysis_request_time'] = analysis_date
    df.loc[:, 'cust_id'] = 7
    # Hardcoded as of now but we will get it from customer_name field in frontend
    # Use function get_end_customer_id_from_name to get end_cust_id of customer
    # df['end_customer_id'] = 1
    df.loc[:, 'end_customer_id'] = 1
    # Get the serial number and strip any leading zeros and store both striped
    # and unstriped serial number

    # df['strip_serial'] = df['Serial#'].str.lstrip('0')
    df.loc[:, 'strip_serial'] = df['Serial#'].str.lstrip('0')
    df.loc[:, 'request_id'] = analysis_id
    # added request id to have binding with analysis_ request table

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
    keep_col = ['cust_id', 'type', 'node_id', 'installed_eqpt', 'part_ordering_number',
                'part', 'serial', 'source_part_data', 'aid', 'end_customer_id',
                'node_name', 'strip_serial', 'analysis_request_time', 'request_id']
    df = df[keep_col]

    df.to_sql(name=table_name, con=engine, index=False, if_exists='append')
    print("Loaded Data into table : {0}".format(table_name))


def to_sql_sap_inventory(table_name, df, analysis_date,analysis_id):

    # Analysis datetime will come from frontend to bind with analysis request id
    # For now it would be a current time
    # analysis_date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    #df['analysis_request_time'] = analysis_date
    engine = Configuration.ECLIPSE_DATA_DB_URI
    #df['cust_id'] = 7
    df.loc[:, 'analysis_request_time'] = analysis_date
    df.loc[:, 'cust_id'] = 7
    df.loc[:, 'strip_material_number'] = df['Material Number'].astype(str).str.lstrip('0')
    df.loc[:, 'request_id'] = analysis_id
    #df['strip_material_number'] = df['Material Number'].astype(str).str.lstrip('0')
    df.rename(columns={
        'Plant': 'plant_id',
        'Storage Location = Depot Name': 'storage_location',
        'Material Number': 'material_number',
        'Material Description = Part Name': 'material_desc',
        'Total Stock': 'total_stock',
        'Reorder Point': 'reorder_point',
        'Standard Cost': 'std_cost',
        'Total Standard Cost': 'total_std_cost',
        'STO - Qty To be Dlv.': 'sto_qty',
        'Delivery - Qty To be Dlv.': 'del_qty',
        'Node Name': 'node_name'
    }, inplace=True
    )
    df.to_sql(name=table_name, con=engine, index=False, if_exists='append')
    print("Loaded Data into table : {0}".format(table_name))


def to_sql_summarytable(table_name, df):
    engine = Configuration.ECLIPSE_DATA_DB_URI
    df.loc[:, 'cust_id'] = 7
    df.loc[:, 'summary_table'] = 1
    # df['cust_id'] = 7
    # df['summary_table'] = 1
    df.rename(columns={
        'material_number_x' : 'material_number',
        'standard_cost_x' : 'standard_cost'
    }, inplace=True
    )
    keep_col = ['cust_id', 'summary_table', 'PON', 'material_number', 'Qty','standard_cost','gross table count','extd std cost','High Spares?','net depot count','net extd std cost']
    df = df[keep_col]
    df.to_sql(name=table_name, con=engine, index=False, if_exists='append')
    print("Loaded Data into table : {0}".format(table_name))


def to_sql_error(table_name, df, invalid_reason, analysis_date, analysis_id):

    engine = Configuration.ECLIPSE_DATA_DB_URI
    # Analysis datetime will come from frontend to bind with analysis request id
    # For now it would be a current time
    # analysis_date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    #df['analysis_request_time'] = analysis_date
    #df['cust_id'] = 7
    df.loc[:, 'analysis_request_time'] = analysis_date
    df.loc[:, 'cust_id'] = 7
    df.loc[:, 'error_reason'] = invalid_reason
    df.loc[:, 'request_id'] = analysis_id
    df.rename(columns={
        'Product Ordering Name': 'PON',
        'Node Name': 'node_name',
        'Node ID': "node_id",
        '#Type': 'type',
        'AID': 'aid',
        'InstalledEqpt': 'installed_eqpt',
        'Part#': 'part',
        'Serial#': 'serial'
    }, inplace=True
    )
    df = df.drop(['Source', 'Valid'], 1)
    df.to_sql(name=table_name, con=engine, index=False, if_exists='append')
    print("Loaded Data into table : {0}".format(table_name))


def process_error_pon(table_name, df, analysis_date, analysis_id):

    engine = Configuration.ECLIPSE_DATA_DB_URI
    # Analysis datetime will come from frontend to bind with analysis request id
    # For now it would be a current time
    # analysis_date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    #df['analysis_request_time'] = analysis_date
    df.loc[:, 'analysis_request_time'] = analysis_date
    df.loc[:, 'cust_id'] = 7
    #df['cust_id'] = 7
    df.loc[: , 'request_id'] = analysis_id
    df = df.drop(['end_customer_node_belongs', 'node_depot_belongs', 'standard_cost',
                   'Valid', 'is_sparrable', 'node_name', 'node_id', 'material_number'], 1)
    for index, row in df.iterrows():
        if row['has_node_depot'] == False:
            df.loc[index, 'error_reason'] = 'PON with no depot'
        elif row['has_std_cost'] == False:
            df.loc[index, 'error_reason'] = 'PON with no std cost'

    df.rename(columns={
        'Product Ordering Name': 'PON',
        'Node Name': 'node_name',
        'Node ID': "node_id",
        '#Type': 'type',
        'AID': 'aid',
        'InstalledEqpt': 'installed_eqpt',
        'Part#': 'part',
        'Serial#': 'serial'
    }, inplace=True
    )
    df = df.drop(['has_node_depot', 'has_std_cost'], 1)
    df.to_sql(name=table_name, con=engine, index=False, if_exists='append')
    print("Loaded Data into table : {0}".format(table_name))




def validate_pon(pon, analysis_date, analysis_id):

    pon['Valid'] = True
    invalid_list = ["", "none", "n/a", "null", "chassis", "unknown", "@", ".."]
    pon.loc[pon['Product Ordering Name'].isin(invalid_list), 'Valid'] = False
    pon.loc[pon['InstalledEqpt'].isin(invalid_list), 'Valid'] = False
    valid_pon = pon[pon['Valid'] == True]
    invalid_pon = pon[pon['Valid'] == False]
    if not invalid_pon.empty:
        to_sql_error('error_records', invalid_pon, "Invalid Pon Name or Invalid Depo", analysis_date, analysis_id)
    return valid_pon


def validate_depot(pon, analysis_date, analysis_id):

    invalid_list = ["not 4hr", "not supported", "nan", "n/a"]
    pon.loc[pon['Node Name'].str.lower().isin(invalid_list), 'Valid'] = False
    # if depot is null are null make it invalid
    pon['node_depot_belongs'] = pon['node_depot_belongs'].fillna("not 4hr")
    pon.loc[pon['node_depot_belongs'].str.lower().isin(invalid_list), 'Valid'] = False
    valid_pon = pon[pon['Valid'] == True]
    invalid_pon = pon[pon['Valid'] == False]
    invalid_pon = invalid_pon[['#Type', 'Node ID', 'Node Name', 'AID', 'InstalledEqpt',
                           'Product Ordering Name', 'Part#', 'Serial#', 'Source', 'Valid']]
    if not invalid_pon.empty:
        to_sql_error('error_records', invalid_pon, "Invalid Node Name", analysis_date, analysis_id)

    return valid_pon


def fetch_db(replenish_time):
    print('fetching data from db...')
    connection = Configuration.ECLIPSE_DATA_DB_URI
    get_misnomer_sql = "SELECT mp.misnomer_pon_name, pt.part_name FROM `Misnomer PON Conversion` mp, `parts` pt where mp.correct_part_id = pt.part_id ;"
    get_standard_cost = "select pt.part_name,pt.material_number,pid.standard_cost from parts pt " \
                        "left join `part cost ID`pid on pt.part_id =pid.part_id where part_name != 'null'"

    get_node = "SELECT * FROM node;"

    # to_sql_customer_dna_record('customer_dna_record', input_db)

    # dump input_db as it is in table INPUT_DB
    misnomer_pons = read_data(get_misnomer_sql, connection)
    standard_cost = read_data(get_standard_cost, connection)
    node = read_data(get_node, connection)

    spared_sql = "SELECT part_name FROM parts where spared_attribute = 1;"
    spared_pons = read_data(spared_sql, connection)

    high_spare_sql = "SELECT pt.part_name, given_spare_part_id, high_spare_part_id FROM high_spare, parts pt where given_spare_part_id = pt.part_id;"
    highspares = read_data(high_spare_sql, connection)

    get_ratio_to_pon_sql = "SELECT * FROM failure_information where failure_name = '{0}'".format(replenish_time)
    print(get_ratio_to_pon_sql)

    get_ratio_to_pon = read_data(get_ratio_to_pon_sql, connection)

    get_parts_sql = 'SELECT * FROM parts;'
    parts = read_data(get_parts_sql, connection)

    get_parts_cost_sql = "SELECT * FROM `part cost ID` pid, parts pt where  pt.material_number = pid.material_number;"
    parts_cost = read_data(get_parts_cost_sql, connection)

    get_high_spares = "select pt1.part_name, pt2.part_name as high_spare from high_spare t " \
                      "inner join parts pt1 on pt1.part_id = t.given_spare_part_id " \
                      "inner join parts pt2 on pt2.part_id = t.high_spare_part_id;"
    high_spares = read_data(get_high_spares, connection)

    get_depot_sql = "SELECT * FROM depot;"
    depot = read_data(get_depot_sql, connection)

    return misnomer_pons, standard_cost, node, spared_pons, highspares, get_ratio_to_pon, parts, parts_cost, high_spares, depot


def get_end_customer_id_from_name():
    engine = create_engine(Configuration.ECLIPSE_DATA_DB_URI)
    query = "select (end_cust_id) from end_customer where end_cust_name='{}'".format("Centurylink")
    result = engine.execute(query).fetchone()
    return result[0]



def add_hnad(df,quantity):

    unique_part_name = df['Product Ordering Name'].unique().tolist()
    for part in unique_part_name:
        di = {}
        di.update({'Product Ordering Name': part, 'node_depot_belongs': 'HNAD', 'PON Quanity': quantity})
        df = df.append(di, ignore_index=True)

    return df


def to_sql_bom(table_name, df, analysis_date, analysis_id):

    engine = Configuration.ECLIPSE_DATA_DB_URI
    # Analysis datetime will come from frontend to bind with analysis request id
    # For now it would be a current time
    # analysis_date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    # df['analysis_request_time'] = analysis_date
    # df['cust_id'] = 7
    df.loc[:, 'analysis_request_time'] = analysis_date
    df.loc[:, 'cust_id'] = 7
    df.loc[:, 'request_id'] = analysis_id
    df.rename(columns={
        'Product Ordering Name': 'part_name',
        'node_depot_belongs': 'depot_name',
        'PON Quanity': 'pon_quantity',
    }, inplace=True
    )


    df.to_sql(name=table_name, con=engine, index=False, if_exists='append')
    print("Loaded Data into table : {0}".format(table_name))


def to_sql_mtbf(table_name, df, analysis_date, analysis_id):
    engine = create_engine(Configuration.ECLIPSE_DATA_DB_URI)
    # Analysis datetime will come from frontend to bind with analysis request id
    # For now it would be a current time
    # analysis_date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    # df['analysis_request_time'] = analysis_date
    # df['cust_id'] = 7
    df.loc[:, 'analysis_request_time'] = analysis_date
    df.loc[:, 'cust_id'] = 7
    df.loc[:, 'request_id'] = analysis_id
    df.rename(columns={
        'Product Ordering Name': 'part_name',
        'node_depot_belongs': 'depot_name',
        'PON Quanity': 'pon_quantity',
    }, inplace=True
    )
    df['pon_quantity'] = df['pon_quantity'].astype(int)
    df.to_sql(name=table_name, con=engine, index=False, if_exists='append')
    print("Loaded Data into table : {0}".format(table_name))


def read_sap_export_file(sap_file):

    sap_inventory_data = pd.read_excel(sap_file, sheet_name='Sheet1')
    return sap_inventory_data


def to_sql_current_ib(table_name, df, analysis_id):

    engine = create_engine(Configuration.ECLIPSE_DATA_DB_URI)
    df.loc[:, 'request_id'] = analysis_id
    df.rename(columns={
        'Product Ordering Name': 'product_ordering_name',
        'PON Quanity': 'pon_quanity',
    }, inplace=True
    )
    df['pon_quanity'] = df['pon_quanity'].astype(int)
    df.to_sql(name=table_name, con=engine, index=False, if_exists='append')
    print("Loaded Data into table : {0}".format(table_name))


def to_sql_part_table(df):
    df['cust_id'] = 7
    df['part_number'] = 0
    df.to_sql(name='parts', con=engine, index=False, if_exists='append', chunksize=1000)
    print("Loaded into parts table")


def to_sql_std_cost_table(df):
    df.to_sql(name='part cost ID', con=engine, index=False, if_exists='append', chunksize=1000)
    print("Loaded into std_cost table")


def to_sql_depot_table(df):
    df.loc[:, 'cust_id'] = 7
    df.to_sql(name='depot', con=engine, index=False, if_exists='append', chunksize=1000)
    print("Loaded into depot table")


def to_sql_node_table(df):
    df.loc[:, 'cust_id'] = 7
    df.to_sql(name='node', con=engine, index=False, if_exists='append', chunksize=1000)
    print("Loaded into node table")


def to_sql_end_customer_table(df):
    df.loc[:, 'end_cust_site_count'] = df.groupby('end_customer_node_belongs')['node_name'].transform('count')
    df.loc[:, 'cust_id'] = 7
    df.loc[:, 'end_cust_status'] = 'Active'

    df.drop(['node_name', 'node_depot_belongs'], axis=1, inplace=True)
    df.rename(columns={
        'end_customer_node_belongs': 'end_cust_name'
    }, inplace=True
    )
    df.drop_duplicates(subset="end_cust_name", inplace=True, keep="first")
    df.to_sql(name='end_customer', con=engine, index=False, if_exists='append', chunksize=1000)
    print("Loaded into end_customer table")


def to_sql_high_spare_table(df):
    df.to_sql(name='high_spare', con=engine, index=False, if_exists='append', chunksize=1000)
    print("Loaded into high_spare table")


def to_sql_misnomer_table(df):
    df.loc[:, 'cust_id'] = 7
    df.rename(columns={
        'Misnomer PON': 'misnomer_pon_name',
        'part_id': 'correct_part_id',
        'cust_id': 'eKryp_cust_id'
        }, inplace=True
              )
    df.to_sql(name='Misnomer PON Conversion', con=engine, index=False, if_exists='append', chunksize=1000)
    print("Loaded into Misnomer table")


def to_sql_failure_information_table(df):
    df.rename(columns={
        'Products': 'product_family',

    }, inplace=True
    )
    df.to_sql(name='failure_information', con=engine, index=False, if_exists='append', chunksize=1000)
    print("Loaded into failure_information table")










