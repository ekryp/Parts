from app import app
from app import csvs, excel, mytext
from flask import jsonify
from flask import request
from sqlalchemy import create_engine
from flask_restful import Resource
from flask_restful import reqparse
from app.utils.utils import get_df_from_sql_query
import pandas as pd
import pdb
import os
import json
from app import Configuration

class GetParts(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('part_name',  location='form')
        self.reqparse.add_argument('material_number', location='form')
        self.reqparse.add_argument('standard_cost', location='form')
        self.reqparse.add_argument('spared_attribute', location='form')
        self.reqparse.add_argument('part_reliability_class', location='form')
        
        self.reqparse.add_argument('parts_id', type=int,required=False, help='parts_id', location='args')
        super(GetParts, self).__init__()

    def patch(self):
        args = self.reqparse.parse_args()
        parts_id = args['parts_id']
        material_number = args['material_number']
        standard_cost = args['standard_cost']
        part_reliability_class = args['part_reliability_class']
        part_name = args['part_name']
        spared_attribute = args['spared_attribute']
        try:
            query = "update parts set material_number='{0}',part_name='{1}',part_reliability_class='{2}',spared_attribute={3} where part_id={4}".format(material_number,part_name,part_reliability_class,spared_attribute,parts_id)
            engine = create_engine(Configuration.INFINERA_DB_URL, echo=False)
            engine.execute(query)
            part_cost_query ="update part_cost set standard_cost={0} where part_id={1}".format(standard_cost,parts_id)
            engine.execute(part_cost_query)
            return jsonify(msg="Parts Details Updated Successfully", http_status_code=200)
        except:
            return jsonify(msg="Error in Inserting,Please try again", http_status_code=400)

    
    def put(self):
        args = self.reqparse.parse_args()
        material_number = args['material_number']
        standard_cost = args['standard_cost']
        part_reliability_class = args['part_reliability_class']
        part_name = args['part_name']
        spared_attribute = args['spared_attribute']
        try:

            query = "INSERT INTO parts (cust_id,material_number,part_name,"\
                    "part_reliability_class,spared_attribute,part_number) values ({0},{1},'{2}','{3}','{4}',{5})".format(7,material_number,part_name,part_reliability_class,spared_attribute,0)
            engine = create_engine(Configuration.INFINERA_DB_URL,echo=False)
            engine.execute(query)
            part_cost_query="INSERT INTO part_cost (part_id,material_number,standard_cost) values ((SELECT part_id FROM parts where part_name='{0}'),{1},{2})".format(part_name,material_number,standard_cost)
            engine.execute(part_cost_query)
            return jsonify(msg="Inserted Successfully", http_status_code=200)
        except:
            return jsonify(msg="Error in Inserting,Please try again", http_status_code=400)


    def get(self):
        query = "select parts.part_id,parts.part_name,parts.material_number,"\
                " part_cost.standard_cost,parts.part_number,"\
                "parts.part_reliability_class,parts.spared_attribute"\
                " from parts inner join part_cost on parts.part_id=part_cost.part_id"

        result = get_df_from_sql_query(
            query=query,
            db_connection_string=Configuration.INFINERA_DB_URL)

        result = result.loc[:, ~result.columns.duplicated()]
        #Removes duplicate column names not column values
        response = json.loads(result.to_json(orient="records", date_format='iso'))
        return response


        
    def options(self):
            return
    
    def delete(self):
        args = self.reqparse.parse_args()
        parts_id = args['parts_id']
        try:

            query = "delete from parts where part_id = {0}".format(parts_id)
            engine = create_engine(Configuration.INFINERA_DB_URL, echo=False)
            result=engine.execute(query)
            print("result",str(result))
            return jsonify(msg="Parts Details Deleted Successfully", http_status_code=200)
        except:
            return jsonify(msg="Error in Deleting,Please try again", http_status_code=400)

    


class GetHighSpare(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('SubstitutionPON',  location='form')
        self.reqparse.add_argument('ClassicPON', location='form')
        self.reqparse.add_argument('high_spare_id', type=str,required=False, help='high_spare_id', location='args')
        super(GetHighSpare, self).__init__()

    def options(self):
            return

    def patch(self):
        args = self.reqparse.parse_args()
        SubstitutionPON = args['SubstitutionPON']
        ClassicPON = args['ClassicPON']
        high_spare_id = args['high_spare_id']
        try:
            query = "update high_spare set given_spare_part_id=(SELECT part_id FROM parts where part_name='{0}'),high_spare_part_id=(SELECT part_id FROM parts where part_name='{1}')  where high_spare_id = {2}".format(ClassicPON,SubstitutionPON,high_spare_id)
            engine = create_engine(Configuration.INFINERA_DB_URL, echo=False)
            engine.execute(query)
            return jsonify(msg="High Spare Updated Details Successfully", http_status_code=200)
        except:
            return jsonify(msg="Error in Inserting,Please try again", http_status_code=400)


    def put(self):
        args = self.reqparse.parse_args()
        ClassicPON = args['ClassicPON']
        SubstitutionPON = args['SubstitutionPON']
        try:
            engine = create_engine(Configuration.INFINERA_DB_URL,echo=False)
            part_cost_query="Insert into high_spare (cust_id,given_spare_part_id,high_spare_part_id) values ({0},(SELECT part_id FROM parts where part_name='{1}'),(SELECT part_id FROM parts where part_name='{2}'))".format(7,ClassicPON,SubstitutionPON)
            engine.execute(part_cost_query)
            return jsonify(msg="Inserted High Spare Details Successfully", http_status_code=200)
        except:
            return jsonify(msg="Error in Inserting,Please try again", http_status_code=400)


    def get(self):
        query = "select t1.part_name as ClassicPON, t2.part_name as SubstitutionPON, t.given_spare_part_id, t.high_spare_id " \
                "from high_spare t"\
                " inner join parts t1 on t1.part_id = t.given_spare_part_id"\
                " inner join parts t2 on t2.part_id = t.high_spare_part_id"

        result = get_df_from_sql_query(
            query=query,
            db_connection_string=Configuration.INFINERA_DB_URL)

        result = result.loc[:, ~result.columns.duplicated()]
        #Removes duplicate column names not column values
        response = json.loads(result.to_json(orient="records", date_format='iso'))
        return response

   
    
    def delete(self):
        args = self.reqparse.parse_args()
        high_spare_id = args['high_spare_id']
        try:

            query = "delete from high_spare where high_spare_id = {0}".format(high_spare_id)
            engine = create_engine(Configuration.INFINERA_DB_URL, echo=False)
            result=engine.execute(query)
            print("result",str(result))
            #result = result.loc[:, ~result.columns.duplicated()]
            #Removes duplicate column names not column values
            
            return jsonify(msg="Deleted High Spare Details Successfully", http_status_code=200)
        except:
            return jsonify(msg="Error in Deleting,Please try again", http_status_code=400)



class GetNode(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('node_name',  location='form')
        self.reqparse.add_argument('end_customer_node_belongs', location='form')
        self.reqparse.add_argument('node_depot_belongs', location='form')
        self.reqparse.add_argument('node_id', type=str,required=False, help='node_id', location='args')
        super(GetNode, self).__init__()


    
    def patch(self):
        args = self.reqparse.parse_args()
        node_name = args['node_name']
        end_customer_node_belongs = args['end_customer_node_belongs']
        node_id = args['node_id']
        node_depot_belongs = args['node_depot_belongs']
        try:
            query = "update node set node_name='{0}',end_customer_node_belongs='{1}',node_depot_belongs='{2}' where node_id={3}".format(node_name,end_customer_node_belongs,node_depot_belongs,node_id)
            engine = create_engine(Configuration.INFINERA_DB_URL, echo=False)
            engine.execute(query)
            return jsonify(msg=" Node Details Updated Successfully", http_status_code=200)
        except:
            return jsonify(msg="Error in Updating,Please try again", http_status_code=400)

    def put(self):
        args = self.reqparse.parse_args()
        node_name = args['node_name']
        end_customer_node_belongs = args['end_customer_node_belongs']
        node_depot_belongs = args['node_depot_belongs']
        try:
            engine = create_engine(Configuration.INFINERA_DB_URL,echo=False)
            query="insert into node (cust_id,node_name,end_customer_node_belongs,node_depot_belongs) values({0},'{1}','{2}','{3}')".format(7,node_name,end_customer_node_belongs,node_depot_belongs)
            engine.execute(query)
            return jsonify(msg="Inserted Node Details Successfully", http_status_code=200)
        except:
            return jsonify(msg="Error in Inserting,Please try again", http_status_code=400)

    def get(self):
        query = "SELECT node.node_id,node.node_name,node.end_customer_node_belongs,node.node_depot_belongs FROM node"

        result = get_df_from_sql_query(
            query=query,
            db_connection_string=Configuration.INFINERA_DB_URL)

        result = result.loc[:, ~result.columns.duplicated()]
        #Removes duplicate column names not column values
        response = json.loads(result.to_json(orient="records", date_format='iso'))
        return response

    

    def delete(self):
        args = self.reqparse.parse_args()
        node_id = args['node_id']
        try:

            query = "delete from node where node_id = {0}".format(node_id)
            engine = create_engine(Configuration.INFINERA_DB_URL, echo=False)
            result=engine.execute(query)
            print("result",str(result))
            #result = result.loc[:, ~result.columns.duplicated()]
            #Removes duplicate column names not column values
            
            return jsonify(msg=" Node Details Deleted Successfully", http_status_code=200)
        except:
            return jsonify(msg="Error in Deleting,Please try again", http_status_code=400)


    def options(self):
            return


class GetDepot(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('depot_name',  location='form')
        self.reqparse.add_argument('depot_address', location='form')
        self.reqparse.add_argument('city', location='form')
        self.reqparse.add_argument('state', location='form')
        self.reqparse.add_argument('country', location='form')
        self.reqparse.add_argument('region',  location='form')
        self.reqparse.add_argument('hub', location='form')
        self.reqparse.add_argument('partner', location='form')
        self.reqparse.add_argument('partner_warehouse_code', location='form')
        self.reqparse.add_argument('contact', location='form')
        self.reqparse.add_argument('lat', location='form')
        self.reqparse.add_argument('long', location='form')
        self.reqparse.add_argument('depot_id', type=str,required=False, help='depot_id', location='args')
        super(GetDepot, self).__init__()

    def put(self):
        args = self.reqparse.parse_args()
        depot_name = args['depot_name']
        depot_address = args['depot_address']
        city = args['city']
        state = args['state']
        country = args['country']
        region = args['region']
        hub = args['hub']
        partner = args['partner']
        partner_warehouse_code = args['partner_warehouse_code']
        contact = args['contact']
        lat = args['lat']
        longitude = args['long']
        try:   
            engine = create_engine(Configuration.INFINERA_DB_URL,echo=False)
            query = "insert into depot (cust_id,depot_name,depot_address,city,state,country,region,hub,partner,partner_warehouse_code,contact,lat,`long`) values({0},'{1}','{2}','{3}','{4}','{5}','{6}',{7},'{8}','{9}','{10}','{11}','{12}')".format(7,depot_name,depot_address,city,state,country,region,hub,partner,partner_warehouse_code,contact,lat,longitude)
            engine.execute(query)
            return jsonify(msg="Inserted Depot Details Successfully", http_status_code=200)
        except:
            return jsonify(msg="Error in Inserting,Please try again", http_status_code=400)

    def patch(self):
        args = self.reqparse.parse_args()
        depot_name = args['depot_name']
        depot_address = args['depot_address']
        city = args['city']
        state = args['state']
        country = args['country']
        region = args['region']
        hub = args['hub']
        partner = args['partner']
        partner_warehouse_code = args['partner_warehouse_code']
        contact = args['contact']
        lat = args['lat']
        longitude = args['long']
        depot_id = args['depot_id']
        try:

            engine = create_engine(Configuration.INFINERA_DB_URL,echo=False)
            query = "update  depot set depot_name = '{0}',depot_address = '{1}',city ='{2}',state ='{3}',country ='{4}',region = '{5}',hub = {6},partner = '{7}',partner_warehouse_code = '{8}',contact ='{8}',lat ='{10}',`long` ='{11}' where depot_id ={12}".format(depot_name,depot_address,city,state,country,region,hub,partner,partner_warehouse_code,contact,lat,longitude,depot_id)
            engine.execute(query)
            return jsonify(msg=" Depot Details Updated Successfully", http_status_code=200)
        except:
            return jsonify(msg="Error in Updating,Please try again", http_status_code=400)

    def get(self):
        query = "SELECT depot_id,depot_name,depot_address,city,state,country,region,hub,partner,partner_warehouse_code,contact,lat,depot.long FROM depot"
        result = get_df_from_sql_query(
            query=query,
            db_connection_string=Configuration.INFINERA_DB_URL)

        result = result.loc[:, ~result.columns.duplicated()]
        #Removes duplicate column names not column values
        response = json.loads(result.to_json(orient="records", date_format='iso'))
        return response

    
    def options(self):
            return

    def delete(self):
        args = self.reqparse.parse_args()
        depot_id = args['depot_id']
        try:

            query = "delete from depot where depot_id = {0}".format(depot_id)
            engine = create_engine(Configuration.INFINERA_DB_URL, echo=False)
            result=engine.execute(query)
            print("result",str(result))
            #result = result.loc[:, ~result.columns.duplicated()]
            #Removes duplicate column names not column values
            
            return jsonify(msg=" Depot Details Deleted Successfully", http_status_code=200)
        except:
            return jsonify(msg="Error in Deleting,Please try again", http_status_code=400)



class GetMisnomer(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('Misnomer_PON',  location='form')
        self.reqparse.add_argument('Correct_PON', location='form')
        self.reqparse.add_argument('reference_table_id', type=str,required=False, help='reference_table_id', location='args')
        super(GetMisnomer, self).__init__()


    
    def patch(self):
        args = self.reqparse.parse_args()
        Misnomer_PON = args['Misnomer_PON']
        Correct_PON = args['Correct_PON']
        reference_table_id = args['reference_table_id']
        try:
            query = "update misnomer_part_conversion set misnomer_part_name='{0}',correct_part_id=(SELECT part_id FROM parts where part_name='{1}')  where reference_table_id = {2}".format(Misnomer_PON,Correct_PON,reference_table_id)
            engine = create_engine(Configuration.INFINERA_DB_URL, echo=False)
            engine.execute(query)
            return jsonify(msg="Misonomer Details Updated Successfully", http_status_code=200)
        except:
            return jsonify(msg="Error in Updating,Please try again", http_status_code=400)

    def put(self):
        args = self.reqparse.parse_args()
        Misnomer_PON = args['Misnomer_PON']
        Correct_PON = args['Correct_PON']
        try:       
            engine = create_engine(Configuration.INFINERA_DB_URL,echo=False)
            query="Insert into misnomer_part_conversion (cust_id,misnomer_part_name,correct_part_id) values ({0},'{1}',(SELECT part_id FROM parts where part_name='{2}'))".format(7,Misnomer_PON,Correct_PON)
            engine.execute(query)
            return jsonify(msg="Inserted Misonomer Details Successfully", http_status_code=200)
        except:
            return jsonify(msg="Error in Inserting,Please try again", http_status_code=400)



    def get(self):
        query = "select t1.part_name as Correct_PON, t.misnomer_part_name as Misnomer_PON, t.reference_table_id,t1.part_id "\
                " from misnomer_part_conversion t"\
                " inner join parts t1 on t1.part_id = t.correct_part_id"
        result = get_df_from_sql_query(
            query=query,
            db_connection_string=Configuration.INFINERA_DB_URL)

        result = result.loc[:, ~result.columns.duplicated()]
        #Removes duplicate column names not column values
        response = json.loads(result.to_json(orient="records", date_format='iso'))
        return response


    def delete(self):
        args = self.reqparse.parse_args()
        reference_table_id = args['reference_table_id']
        try:
            query = "delete from misnomer_part_conversion where reference_table_id = {0}".format(reference_table_id)
            engine = create_engine(Configuration.INFINERA_DB_URL, echo=False)
            result=engine.execute(query)
            print("result",str(result))
            #result = result.loc[:, ~result.columns.duplicated()]
            #Removes duplicate column names not column values
            
            return jsonify(msg="Deleted Misonomer Details Successfully", http_status_code=200)
        except:
            return jsonify(msg="Error in Deleting,Please try again", http_status_code=400)


    def options(self):
            return

class GetRatio(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('replenish_time',  location='form')
        self.reqparse.add_argument('product_family', location='form')
        self.reqparse.add_argument('number_of_spares_1', location='form')
        self.reqparse.add_argument('number_of_spares_2', location='form')
        self.reqparse.add_argument('number_of_spares_3', location='form')
        self.reqparse.add_argument('number_of_spares_4',  location='form')
        self.reqparse.add_argument('number_of_spares_5', location='form')
        self.reqparse.add_argument('number_of_spares_6', location='form')
        self.reqparse.add_argument('number_of_spares_7', location='form')
        self.reqparse.add_argument('number_of_spares_8', location='form')
        self.reqparse.add_argument('number_of_spares_9', location='form')
        self.reqparse.add_argument('number_of_spares_10', location='form')
        self.reqparse.add_argument('pon_type', type=str,required=True, help='pon_type', location='args')
        self.reqparse.add_argument('reliability_id', type=str,required=False, help='reliability_id', location='args')
        super(GetRatio, self).__init__()
    

    def put(self):
        args = self.reqparse.parse_args()
        pon_type = args['pon_type']
        product_family = args['product_family']
        number_of_spares_1 = args['number_of_spares_1']
        number_of_spares_2 = args['number_of_spares_2']
        number_of_spares_3 = args['number_of_spares_3']
        number_of_spares_4 = args['number_of_spares_4']
        number_of_spares_5 = args['number_of_spares_5']
        number_of_spares_6 = args['number_of_spares_6']
        number_of_spares_7 = args['number_of_spares_7']
        number_of_spares_8 = args['number_of_spares_8']
        number_of_spares_9 = args['number_of_spares_9']
        number_of_spares_10 = args['number_of_spares_10']
        try:
            engine = create_engine(Configuration.INFINERA_DB_URL,echo=False)
            query="Insert into reliability_class (cust_id,replenish_time,product_family,`1`,`2`,`3`,`4`,`5`,`6`,`7`,`8`,`9`,`10`) values({0},'{1}','{2}',{3},{4},{5},{6},{7},{8},{9},{10},{11},{12})".format(7,pon_type,product_family,number_of_spares_1,number_of_spares_2,number_of_spares_3,number_of_spares_4,number_of_spares_5,number_of_spares_6,number_of_spares_7,number_of_spares_8,number_of_spares_9,number_of_spares_10)
            engine.execute(query)
            return jsonify(msg="Inserted Ratio PON Details Successfully", http_status_code=200)
        except:
            return jsonify(msg="Error in Inserting,Please try again", http_status_code=400)


    def patch(self):
        args = self.reqparse.parse_args()
        pon_type = args['pon_type']
        product_family = args['product_family']
        reliability_id = args['reliability_id']
        number_of_spares_1 = args['number_of_spares_1']
        number_of_spares_2 = args['number_of_spares_2']
        number_of_spares_3 = args['number_of_spares_3']
        number_of_spares_4 = args['number_of_spares_4']
        number_of_spares_5 = args['number_of_spares_5']
        number_of_spares_6 = args['number_of_spares_6']
        number_of_spares_7 = args['number_of_spares_7']
        number_of_spares_8 = args['number_of_spares_8']
        number_of_spares_9 = args['number_of_spares_9']
        number_of_spares_10 = args['number_of_spares_10']
        try:

            engine = create_engine(Configuration.INFINERA_DB_URL,echo=False)
            query="Update reliability_class set replenish_time='{0}',product_family='{1}',`1`={2},`2`={3},`3`={4},`4`={5},`5`={6},`6`={7},`7`={8},`8`={9},`9`={10},`10`={11} where reliability_id={12}".format(pon_type,product_family,number_of_spares_1,number_of_spares_2,number_of_spares_3,number_of_spares_4,number_of_spares_5,number_of_spares_6,number_of_spares_7,number_of_spares_8,number_of_spares_9,number_of_spares_10,reliability_id)
            engine.execute(query)
            return jsonify(msg=" Ratio PON Details Updated Successfully", http_status_code=200)
        except:
            return jsonify(msg="Error in Updating,Please try again", http_status_code=400)


    
    def get(self):
        args = self.reqparse.parse_args()
        pon_type = args['pon_type']
        query = "SELECT reliability_id,product_family,`1`  as number_of_spares1,`2`  as number_of_spares2,`3`  as number_of_spares3,`4`  as number_of_spares4,`5`  as number_of_spares5,`6`  as number_of_spares6,`7`  as number_of_spares7,`8`  as number_of_spares8,`9`  as number_of_spares9,`10`  as number_of_spares10 FROM reliability_class WHERE replenish_time = '{0}'".format(pon_type)
        result = get_df_from_sql_query(
            query=query,
            db_connection_string=Configuration.INFINERA_DB_URL)

        result = result.loc[:, ~result.columns.duplicated()]
        #Removes duplicate column names not column values
        response = json.loads(result.to_json(orient="records", date_format='iso'))
        return response

    def delete(self):
        args = self.reqparse.parse_args()
        reliability_id = args['reliability_id']
        try:
            
            query = "delete from reliability_class where reliability_id = {0}".format(reliability_id)
            engine = create_engine(Configuration.INFINERA_DB_URL, echo=False)
            result=engine.execute(query)
            print("result",str(result))
            #result = result.loc[:, ~result.columns.duplicated()]
            #Removes duplicate column names not column values
            
            return jsonify(msg=" Ratio PON Details Deleted Successfully", http_status_code=200)
        except:
            return jsonify(msg="Error in Deleting,Please try again", http_status_code=400)

        
    def options(self):
            return