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
from app.configs import Configuration


def get_list_of_files(ekryp_partner_id):
    csv_files = glob.glob('*.csv')
    csv_files.remove("installed_base_{0}.{1}".format(str(ekryp_partner_id), 'csv'))
    csv_files.insert(0,"installed_base_{0}.{1}".format(str(ekryp_partner_id), 'csv'))
    lst_of_files = csv_files[:]
    return lst_of_files


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

def datasource_creation_per_user_per_file(ekryp_partner_id,files,email_id):
    new_datasource_name = os.path.splitext(files)[0]
    copy_from_existing_datasource = '_'.join(new_datasource_name.split('_')[:-1])

    engine = create_engine(Configuration.EKRYP_USER_DB_URI)
    try:
        query = "insert into ekryp_partner (id,status,partner_name) values({0},1,'{1}')".format(ekryp_partner_id,email_id)
        engine.execute(query)
    except exc.IntegrityError as e:
        pass

    try:
        query = """insert into druid_datasources (datasource_name,ekryp_partner_id,description,cluster_name,offset)
                select '{0}','{1}',description,cluster_name,offset
                from druid_datasources where datasource_name = '{2}'""".format(new_datasource_name,ekryp_partner_id,copy_from_existing_datasource)
        engine.execute(query)
        query = "SELECT id,datasource_name FROM druid_datasources where datasource_name = '{}'".format(
            new_datasource_name)
        result = engine.execute(query).fetchone()
        ekryp_datasource_id = result[0]
        datasource_key_mapping = {'incident' : 'incident_new_version', 'installed_base':'installed_base',
                                  'daily_work' : 'daily_work' ,'asset_life_event' :'asset_life_event',
                                  'asset_conditions_events' : 'asset_conditions_events'}
        if ekryp_datasource_id:
            query = "insert into datasource_partner(ekryp_partner_id, ekryp_datasource_id,datasource_key) " \
                    "values({0}, {1},'{2}')".format(ekryp_partner_id, ekryp_datasource_id,
                                                    datasource_key_mapping.get(copy_from_existing_datasource))
            engine.execute(query)

        try:
            query = """insert into druid_columns (
                    datasource_name,column_name,is_active,type,groupby,count_distinct,sum,avg,max,
                    min,filterable,description,dimension_spec_json
                    )
                    select 
                    '{0}',a.column_name,a.is_active,a.type,a.groupby,a.count_distinct,a.sum,a.avg,a.max,
                    a.min,a.filterable,a.description,a.dimension_spec_json 
                    from 
                    druid_columns as a where a.datasource_name="{1}" \
                    """.format(new_datasource_name, copy_from_existing_datasource)
            engine.execute(query)
        except:
            pass
        try:
            query = "insert into metrics (metric_name,verbose_name,metric_type,datasource_name,json,is_restricted) select metric_name,verbose_name,metric_type,'{0}',json,is_restricted from metrics where datasource_name='{1}'".format(
                new_datasource_name, copy_from_existing_datasource)
            engine.execute(query)
        except:
            pass
        # constants_py = ['incident_new_version', 'fops', 'parts_new_version']
        # for datasource_name in constants_py:
        #     new_datasource_name = datasource_name +'_' + str(ekryp_partner_id)
        #     query = """insert into druid_datasources (datasource_name,ekryp_partner_id,description,cluster_name,offset)
        #         values('{0}','{1}',description,'local_dev3',0)
        #              """.format(new_datasource_name, ekryp_partner_id)
        #     engine.execute(query)
        #     query = "SELECT id,datasource_name FROM druid_datasources where datasource_name = '{}'".format(
        #         new_datasource_name)
        #     result = engine.execute(query).fetchone()
        #     ekryp_datasource_id = result[0]
        #     try:
        #         if ekryp_datasource_id:
        #             query = "insert into datasource_partner(ekryp_partner_id, ekryp_datasource_id,datasource_key) " \
        #                 "values({0}, {1},'{2}')".format(ekryp_partner_id, ekryp_datasource_id,
        #                                             datasource_name)
        #             engine.execute(query)
        #     except:
        #         pass
    except exc.IntegrityError as e:
        print("INFO :: Datasource {0} already present for ekryp_partner_id : {1}".format(new_datasource_name,ekryp_partner_id))





def incident_data_creation_per_user_per_file(ekryp_partner_id,files):

    engine = create_engine(Configuration.EKRYP_DATA_DB_URI)
    query = "delete from incident where cust_id ={0}".format(ekryp_partner_id)
    engine.execute(query)
    incidet_df = pd.read_csv(files,index_col=False)
    #added column cust_id in dataframe
    incidet_df['cust_id'] = ekryp_partner_id
    incidet_df =  incidet_df [[
                'cust_id','Service Ticket Number','Serial Number','Service Request Date',
               'Service Request Time','Service Rep','Priority','Incident Category','Initial Reason','Final Reason',
                'Status'
               ]]
    incidet_df.rename(columns = {
        'cust_id':'cust_id',
        'Service Ticket Number':'cust_source_sys_ref','Serial Number':'asset_id',
        'Service Request Date':'incident_date','Service Request Time':'incident_time',
        'Service Rep':'incident_service_rep_name','Priority':'incident_priority',
        'Incident Category':'incident_category','Initial Reason':'incident_initial_reason',
        'Final Reason':'incident_final_reason','Status':'incident_status',
                         },inplace=True
              )
    #Get asset_id from asset table not from csv
    asset_df = pd.read_sql_table('asset', con=engine,columns = ['asset_id','asset_serial_num','cust_id'])
    mask = asset_df['cust_id'] == ekryp_partner_id
    asset_df_for_ekryp_partner_id = asset_df.ix[mask]
    #incidet_df['asset_id'] = asset_df_for_ekryp_partner_id['asset_id']
    incidet_df["asset_id"] = incidet_df["asset_id"].astype(str)
    final_df = pd.merge(incidet_df,asset_df_for_ekryp_partner_id, how="left", left_on="asset_id", right_on="asset_serial_num")
    final_df = final_df[~final_df['asset_id_y'].isnull()]  #remove where asset_id are NULL
    final_df["asset_id"] = final_df["asset_id_y"].astype(int)
    final_df["cust_id"] = final_df["cust_id_x"].astype(int)
    final_df.drop(['asset_serial_num','cust_id_x','cust_id_y','asset_id_x','asset_id_y',], axis=1, inplace=True)

    try:
        final_df.to_sql(name='incident', con =engine, index=False, if_exists='append' )
    except:
        print ("INFO :: Failed to insert in Incident table for {0}".format(ekryp_partner_id))


def installed_base_data_creation_per_user_per_file(ekryp_partner_id,files):
    engine = create_engine(Configuration.EKRYP_DATA_DB_URI)
    query = "delete from asset where cust_id ={0}".format(ekryp_partner_id)
    engine.execute(query)
    df = pd.read_csv(files,index_col=False)
    #added column cust_id in dataframe
    df['cust_id'] = ekryp_partner_id
    df.drop(['Model Group ID','Model Group Name','Category','Category Name','Type Id','type_name'], axis=1, inplace=True)
    df.rename(columns={
        'cust_id': 'cust_id','Serial Number':'asset_serial_num','Firmware ID':'asset_firmware_id',
        'Site ID':'asset_site_id','Warranty End Date':'asset_warranty_end_date',
        'Service Start Date':'asset_service_start_date','Service End Date':'asset_service_end_date',
        'Installed Date':'asset_installed_date','Model_ID':'asset_model_id',
        'Model Name':'asset_model_name','Asset Attribute  Identifier':'asset_id_from_source',
        'Service Provider Id':'asset_partner_id','Product Desc':'asset_desc',
        'Active Status':'asset_status_type_name','Latest Inactive Date':'asset_status_type_date'
                     },inplace=True
            )
    try:
        df.to_sql(name='asset', con=engine, index=False, if_exists='append')
    except:
        print ("INFO :: Failed to insert in installed_base table for {0}".format(ekryp_partner_id))



def asset_life_event_data_creation_per_user_per_file(ekryp_partner_id,files):
    engine = create_engine(Configuration.EKRYP_DATA_DB_URI)
    query = "delete from asset_life_event where cust_id ={0}".format(ekryp_partner_id)
    engine.execute(query)
    asset_life_event_df = pd.read_csv(files, index_col=False)
    asset_life_event_df['ekryp_partner_id'] = ekryp_partner_id
    asset_life_event_df.rename(columns={
        "Serial Number":"asset_id", "Life Event Code":"asset_life_event_type_id", "Event date":"asset_life_event_date",
        'ekryp_partner_id':'cust_id',"Life Event Value":"asset_life_event_type_value"
                        },inplace=True
            )

    #Get asset_id from asset table not from csv
    asset_df = pd.read_sql_table('asset', con=engine,columns = ['asset_id','asset_serial_num','cust_id','asset_id_from_source'])
    mask = asset_df['cust_id'] == ekryp_partner_id
    asset_df_for_ekryp_partner_id = asset_df.ix[mask]
    #incidet_df['asset_id'] = asset_df_for_ekryp_partner_id['asset_id']
    asset_life_event_df["asset_id"] = asset_life_event_df["asset_id"].astype(str)
    final_df = pd.merge(asset_life_event_df,asset_df_for_ekryp_partner_id, how="left", left_on="asset_id", right_on="asset_serial_num")
    final_df = final_df[~final_df['asset_id_y'].isnull()] #remove where asset_id are NULL
    final_df["asset_id"] = final_df["asset_id_y"].astype(int)
    final_df["cust_id"] = final_df["cust_id_x"].astype(int)
    final_df.drop(['asset_serial_num','cust_id_x','cust_id_y','asset_id_x','asset_id_y',], axis=1, inplace=True)

    try:
        final_df.to_sql(name='asset_life_event', con =engine, index=False, if_exists='append' )
    except:
        print ("INFO :: Failed to insert in asset_life_event table for {0}".format(ekryp_partner_id))


def asset_conditions_events_data_creation_per_user_per_file(ekryp_partner_id,files):
    engine = create_engine(Configuration.EKRYP_DATA_DB_URI)
    query = "delete from asset_event where cust_id ={0}".format(ekryp_partner_id)
    engine.execute(query)
    asset_conditions_events_df = pd.read_csv(files,index_col=False)
    #added column cust_id in dataframe
    asset_conditions_events_df['ekryp_partner_id'] = ekryp_partner_id
    asset_conditions_events_df.drop(['Code Detail','Key Value Pairs'], axis=1, inplace=True)
    asset_conditions_events_df.rename(columns={
        'ekryp_partner_id':'cust_id','Serial Number':'asset_id',
        'Date':'event_date','Time':'event_time','Code Id':'event_code_id','Code Type':'event_code_type_id',
        'Code Description':'event_code_desc','Code Criticality':'event_code_criticality',
        'Code':'event_code_value','Code area':'event_code_area'
                        },inplace=True
            )

    asset_df = pd.read_sql_table('asset', con=engine,columns = ['asset_id','asset_serial_num','cust_id'])
    mask = asset_df['cust_id'] == ekryp_partner_id
    asset_df_for_ekryp_partner_id = asset_df.ix[mask]
    asset_conditions_events_df["asset_id"] = asset_conditions_events_df["asset_id"].astype(str)
    final_df = pd.merge(asset_conditions_events_df,asset_df_for_ekryp_partner_id, how="left", left_on="asset_id", right_on="asset_serial_num")
    final_df = final_df[~final_df['asset_id_y'].isnull()]  #remove where asset_id are NULL
    final_df["asset_id"] = final_df["asset_id_y"].astype(int)
    final_df["cust_id"] = final_df["cust_id_x"].astype(int)
    final_df.drop(['asset_serial_num','cust_id_x','cust_id_y','asset_id_x','asset_id_y',], axis=1, inplace=True)

    ###
    try:
        final_df.to_sql(name='asset_event', con=engine, index=False, if_exists='append')
    except:
        print ("INFO :: Failed to insert in asset_event table for {0}".format(ekryp_partner_id))



def daily_work_data_creation_per_user_per_file(ekryp_partner_id,files):
    engine = create_engine(Configuration.EKRYP_DATA_DB_URI)
    query = "delete from dailywork where cust_id ={0}".format(ekryp_partner_id)
    engine.execute(query)
    daily_work_df = pd.read_csv(files, index_col=False)
    daily_work_df['ekryp_partner_id'] = ekryp_partner_id
    daily_work_df.rename(columns={
        "Serial Number":"asset_id", "Date":"dailywork_date", "Time":"dailywork_time",'ekryp_partner_id':'cust_id'
                        },inplace=True
            )

    #Get asset_id from asset table not from csv
    asset_df = pd.read_sql_table('asset', con=engine,columns = ['asset_id','asset_serial_num','cust_id'])
    mask = asset_df['cust_id'] == ekryp_partner_id
    asset_df_for_ekryp_partner_id = asset_df.ix[mask]
    #incidet_df['asset_id'] = asset_df_for_ekryp_partner_id['asset_id']
    daily_work_df["asset_id"] = daily_work_df["asset_id"].astype(str)
    final_df = pd.merge(daily_work_df,asset_df_for_ekryp_partner_id, how="left", left_on="asset_id", right_on="asset_serial_num")
    final_df = final_df[~final_df['asset_id_y'].isnull()] #remove where asset_id are NULL
    final_df["asset_id"] = final_df["asset_id_y"].astype(int)
    final_df["cust_id"] = final_df["cust_id_x"].astype(int)
    final_df.drop(['asset_serial_num','cust_id_x','cust_id_y','asset_id_x','asset_id_y',], axis=1, inplace=True)

    try:
        final_df.to_sql(name='dailywork', con =engine, index=False, if_exists='append' )
    except:
        print ("INFO :: Failed to insert in dailywork table for {0}".format(ekryp_partner_id))


def add_prospect(ekryp_partner_id,email_id):
    engine = create_engine(Configuration.PROSPECT_DB_URL)
    try:
        # delete previous prospect_status's if csv's are uploaded 2 nd time.
        query = "delete FROM prospects_status where prospects_id={0}".format(ekryp_partner_id)
        engine.execute(query)
        query = "insert into prospect_details (prospects_id,prospects_email) values({0},'{1}')".format(ekryp_partner_id,email_id)
        engine.execute(query)
    except exc.IntegrityError as e:
        print("INFO:: Prospect ID: {0} is already registered with us".format(ekryp_partner_id))

def update_prospect_step(step_id,ekryp_partner_id):
    engine = create_engine(Configuration.PROSPECT_DB_URL)
    try:
        query = "insert into prospects_status (prospects_id,prospects_step,updated_date) values({0} ,{1},CURDATE())".format(ekryp_partner_id,
                                                                                                 step_id)
        engine.execute(query)
    except:
        print("Failed to update status for prospects_id {0}".format(ekryp_partner_id))


@celery.task
def task_customer_creation_mysql_ingestion(ekryp_partner_id,email_id):
    dest_folder = str(ekryp_partner_id)
    dir_path = os.path.join(app.config.get("UPLOADED_CSV_DEST"),dest_folder)
    full_path= os.path.abspath(dir_path)
    owd = os.getcwd()
    os.chdir(full_path)

    user_creation_function_call = {
        "incident_{0}.{1}".format(str(ekryp_partner_id), 'csv'): datasource_creation_per_user_per_file,
        "installed_base_{0}.{1}".format(str(ekryp_partner_id), 'csv'): datasource_creation_per_user_per_file,
        "asset_life_event_{0}.{1}".format(str(ekryp_partner_id), 'csv'): datasource_creation_per_user_per_file,
        "asset_conditions_events_{0}.{1}".format(str(ekryp_partner_id), 'csv'): datasource_creation_per_user_per_file,
        "daily_work_{0}.{1}".format(str(ekryp_partner_id), 'csv'): datasource_creation_per_user_per_file
    }
    try:
        lst_of_files = get_list_of_files(ekryp_partner_id)
        for files in lst_of_files:
            try:
                print("USER CREATION for file : {0} & for prospect {1} started".format(files, ekryp_partner_id))
                user_creation_function_call.get(files)(ekryp_partner_id,files,email_id)
            except TypeError:
                pass

        update_prospect_step(2,ekryp_partner_id)
    finally:
        os.chdir(owd)

@celery.task
def task_data_creation_mysql_ingestion(ekryp_partner_id):
    dest_folder = str(ekryp_partner_id)
    dir_path = os.path.join(app.config.get("UPLOADED_CSV_DEST"),dest_folder)
    full_path= os.path.abspath(dir_path)
    owd = os.getcwd()
    os.chdir(full_path)

    data_creation_per_user_per_file = {
        "incident_{0}.{1}".format(str(ekryp_partner_id), 'csv'): incident_data_creation_per_user_per_file,
        "installed_base_{0}.{1}".format(str(ekryp_partner_id), 'csv'): installed_base_data_creation_per_user_per_file,
        "asset_life_event_{0}.{1}".format(str(ekryp_partner_id), 'csv'): asset_life_event_data_creation_per_user_per_file,
        "asset_conditions_events_{0}.{1}".format(str(ekryp_partner_id), 'csv'): asset_conditions_events_data_creation_per_user_per_file,
        "daily_work_{0}.{1}".format(str(ekryp_partner_id), 'csv'): daily_work_data_creation_per_user_per_file
    }
    try:
        lst_of_files = get_list_of_files(ekryp_partner_id)
        #First insert in installed_base then into incident
        for files in lst_of_files:
            try:
                print("SQL INSERTION for file : {0} & for prospect {1} started".format(files,ekryp_partner_id))
                data_creation_per_user_per_file.get(files)(ekryp_partner_id,files)
            except TypeError:
                pass
        update_prospect_step(3, ekryp_partner_id)
    finally:
        os.chdir(owd)


def json_creation_per_user_per_file(ekryp_partner_id,files):
    curr_path = os.getcwd()
    jsons_dir=os.path.join(curr_path,app.config.get("UPLOADED_JSON_DEST"))
    new_json_filename = os.path.splitext(files)[0]
    copy_from_existing_csv_filename = '_'.join(new_json_filename.split('_')[:-1])
    filename = copy_from_existing_csv_filename + '.json'
    json_file_path = os.path.join(jsons_dir,filename)
    f = open(json_file_path)
    data = json.load(f)
    data['spec']['dataSchema']['dataSource'] = new_json_filename
    dest_folder = str(ekryp_partner_id)
    dir_path = os.path.join(app.config.get("UPLOADED_CSV_DEST"), dest_folder)
    json_file = os.path.join(dir_path,new_json_filename + '.json' )
    tsv_folder= os.path.join(Configuration.TSV_DEST,str(ekryp_partner_id))
    tsv_file = os.path.join(tsv_folder,new_json_filename + '.tsv')
    #This is for local testing on windows
    #tsv_file = os.path.join(dir_path, new_json_filename + '.tsv')
    #data['spec']['ioConfig']['inputSpec']['paths'] =os.path.abspath(tsv_file)
    data['spec']['ioConfig']['inputSpec']['paths'] = tsv_file
    with open(json_file, 'w') as fp:
        json.dump(data, fp, indent=4)



@celery.task
def task_json_creation_per_file(ekryp_partner_id,email_id):
    dest_folder = str(ekryp_partner_id)
    dir_path = os.path.join(app.config.get("UPLOADED_CSV_DEST"), dest_folder)
    full_path = os.path.abspath(dir_path)
    owd = os.getcwd()
    os.chdir(full_path)
    json_creation_function_call = {
        "incident_{0}.{1}".format(str(ekryp_partner_id), 'csv'): json_creation_per_user_per_file,
        "installed_base_{0}.{1}".format(str(ekryp_partner_id), 'csv'): json_creation_per_user_per_file,
        "asset_life_event_{0}.{1}".format(str(ekryp_partner_id), 'csv'): json_creation_per_user_per_file,
        "asset_conditions_events_{0}.{1}".format(str(ekryp_partner_id), 'csv'): json_creation_per_user_per_file,
        "daily_work_{0}.{1}".format(str(ekryp_partner_id), 'csv'): json_creation_per_user_per_file
    }
    try:
        lst_of_files = get_list_of_files(ekryp_partner_id)
        os.chdir(owd)
        #First insert in installed_base then into incident
        for files in lst_of_files:
            try:
                print("JSON Creation for file : {0} & for prospect {1} started".format(files,ekryp_partner_id))
                json_creation_function_call.get(files)(ekryp_partner_id,files)
            except TypeError:
                pass
    finally:
        os.chdir(owd)

def tsv_creation_per_user_per_file(ekryp_partner_id,files):

    curr_path = os.getcwd()
    sqls_dir = os.path.join(curr_path, app.config.get("UPLOADED_SQLS_DEST"))
    new_sql_filename = os.path.splitext(files)[0]
    copy_from_existing_csv_filename = '_'.join(new_sql_filename.split('_')[:-1])
    filename = copy_from_existing_csv_filename + '.sql'
    sql_file_path = os.path.join(sqls_dir, filename)
    dest_folder = str(ekryp_partner_id)
    dir_path = os.path.join(app.config.get("UPLOADED_CSV_DEST"), dest_folder)
    tsv_file = os.path.join(dir_path,new_sql_filename + '.tsv' )

    import subprocess
    user = Configuration.MYSQL_USER
    host = Configuration.MYSQL_HOST
    pwd = Configuration.MYSQL_PWD
    db_name = Configuration.MYSQL_DB
    ekryp_partner_id = ekryp_partner_id
    base_sql_file = sql_file_path
    tsv_outfile = tsv_file
    #os.chdir(sqls_dir)
    cmd = 'mysql --skip-column-names -u {0} -h {1} -p{2} -D{3} -e "`sed "s/MYSQL_EKRYP_DB_NAME/{3}/g;s/prospect_id/{4}/g;" < {5}`" > {6}'.format(
        user, host, pwd, db_name,ekryp_partner_id, base_sql_file, tsv_file)
    print(cmd)
    try:
        subprocess.call(cmd, shell=True)
        druid_drive = Configuration.DRUID_DRIVE
        dest = os.path.join(druid_drive,str(ekryp_partner_id))
        if not os.path.isdir(dest):
            os.makedirs(dest)
        copy(tsv_file,dest)
        time.sleep(20)

    except:
        pass
    os.chdir(curr_path)

@celery.task
def task_tsv_creation_per_file(ekryp_partner_id,email_id):
    dest_folder = str(ekryp_partner_id)
    dir_path = os.path.join(app.config.get("UPLOADED_CSV_DEST"), dest_folder)
    full_path = os.path.abspath(dir_path)
    owd = os.getcwd()
    os.chdir(full_path)
    tsv_creation_function_call = {
        "incident_{0}.{1}".format(str(ekryp_partner_id), 'csv'): tsv_creation_per_user_per_file,
        "installed_base_{0}.{1}".format(str(ekryp_partner_id), 'csv'): tsv_creation_per_user_per_file,
        "asset_life_event_{0}.{1}".format(str(ekryp_partner_id), 'csv'): tsv_creation_per_user_per_file,
        "asset_conditions_events_{0}.{1}".format(str(ekryp_partner_id), 'csv'): tsv_creation_per_user_per_file,
        "daily_work_{0}.{1}".format(str(ekryp_partner_id), 'csv'): tsv_creation_per_user_per_file
    }

    try:
        lst_of_files = get_list_of_files(ekryp_partner_id)
        #First insert in installed_base then into incident
        os.chdir(owd)
        for files in lst_of_files:
            try:
                print("TSV Creation for file : {0} & for prospect {1} started".format(files,ekryp_partner_id))
                tsv_creation_function_call.get(files)(ekryp_partner_id,files)
            except TypeError:
                pass

    finally:
        os.chdir(owd)

def druid_ingetion_per_user_per_file(ekryp_partner_id,files):
    owd = os.getcwd()
    dest_folder = str(ekryp_partner_id)
    dir_path = os.path.join(app.config.get("UPLOADED_CSV_DEST"), dest_folder)
    full_path = os.path.abspath(dir_path)
    curr_path = os.getcwd()
    os.chdir(full_path)
    json_file = os.path.splitext(files)[0] +'.json'
    druid_host = Configuration.DRUID_HOST
    # cmd = 'curl -X POST -H Content-Type:application/json -d @{0} {1}'.format(json_file,druid_host)
    # subprocess.call(cmd,shell=True)
    import requests
    headers = {'Content-Type': 'application/json',}
    data = open(json_file)
    response = requests.post(druid_host, headers=headers, data=data)
    time.sleep(300)
    os.chdir(owd)



@celery.task
def task_druid_ingestion_per_file(ekryp_partner_id,email_id):
    dest_folder = str(ekryp_partner_id)
    dir_path = os.path.join(app.config.get("UPLOADED_CSV_DEST"), dest_folder)
    full_path = os.path.abspath(dir_path)
    owd = os.getcwd()
    os.chdir(full_path)
    druid_ingetion_function_call = {
        "incident_{0}.{1}".format(str(ekryp_partner_id), 'csv'): druid_ingetion_per_user_per_file,
        "installed_base_{0}.{1}".format(str(ekryp_partner_id), 'csv'): druid_ingetion_per_user_per_file,
        "asset_life_event_{0}.{1}".format(str(ekryp_partner_id), 'csv'): druid_ingetion_per_user_per_file,
        "asset_conditions_events_{0}.{1}".format(str(ekryp_partner_id), 'csv'): druid_ingetion_per_user_per_file,
        "daily_work_{0}.{1}".format(str(ekryp_partner_id), 'csv'): druid_ingetion_per_user_per_file
    }

    try:
        lst_of_files = get_list_of_files(ekryp_partner_id)
        #First insert in installed_base then into incident
        os.chdir(owd)
        for files in lst_of_files:
            try:
                print("DRUID INGESTION for file : {0} & for prospect {1} started".format(files,ekryp_partner_id))
                druid_ingetion_function_call.get(files)(ekryp_partner_id,files)
            except TypeError:
                pass
        update_prospect_step(4, ekryp_partner_id)
    finally:
        os.chdir(owd)

def send_email(message_text):
	sender = 'Ashish.Bainade@gslab.com'
	receivers = ['aashish.joshi@gslab.com']
	subject = 'Test Email'
	COMMASPACE = ', '
	msg = MIMEText(message_text)
	msg['Subject'] = subject
	msg['From'] = sender
	msg['To'] = COMMASPACE.join(receivers)
	try:
		smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
		smtpObj.starttls()
		smtpObj.login("ashish.bainade@gslab.com", "pwd")
		smtpObj.sendmail(sender, receivers, msg.as_string())
		print("Successfully sent email")
		smtpObj.quit()
	except smtplib.SMTPException:
		print("Error: unable to send email")


@celery.task
def folder_structure_creation(ekryp_partner_id):
    BASE_DIR = Configuration.BASE_DIR
    ONE_STEP_DIRECTORY = ['data', 'experiments']

    def copy_prospect_csv(ekryp_partner_id, copy_destination):
        dest_folder = str(ekryp_partner_id)
        dir_path = os.path.join(app.config.get("UPLOADED_CSV_DEST"), dest_folder)
        owd = os.getcwd()
        os.chdir(os.path.abspath(dir_path))
        csv_files = glob.glob('*.csv')
        for csv in csv_files:
            copy(csv, copy_destination)
        os.chdir(owd)

    def one_step_directory_creation(parent_dir, subfolder_name):
        ABS_BASE_DIR = os.path.abspath(BASE_DIR)
        USER_DIR = os.path.join(ABS_BASE_DIR, str(parent_dir))
        owd = os.getcwd()
        os.chdir(USER_DIR)
        if not os.path.isdir(subfolder_name):
            os.makedirs(subfolder_name)
        os.chdir(owd)

    def create_user_folder(ekryp_partner_id):
        ABS_BASE_DIR = os.path.abspath(BASE_DIR)
        USER_DIR = os.path.join(ABS_BASE_DIR, str(ekryp_partner_id))
        if not os.path.isdir(USER_DIR):
            os.makedirs(USER_DIR)
        for first_level_folder in ONE_STEP_DIRECTORY:
            one_step_directory_creation(ekryp_partner_id, first_level_folder)
        CSV_COPY_FOLDER = os.path.join(USER_DIR, ONE_STEP_DIRECTORY[0])
        copy_prospect_csv(ekryp_partner_id, CSV_COPY_FOLDER)

    create_user_folder(ekryp_partner_id)
    send_email('Test email')

@celery.task
def dummy(a, b):
    print("task1 dummy called")
    import time
    time.sleep(100)
    print("task1 dummy done")
