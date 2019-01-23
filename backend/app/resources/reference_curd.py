from app import app
from app import csvs, excel, mytext
from flask import jsonify
from flask import request
from flask_restful import Resource
from flask_restful import reqparse
from app.utils.utils import get_df_from_sql_query
import pandas as pd
import pdb
import os
import json
from app import Configuration

class GetParts(Resource):

    def get(self):
        query = "select infinera.parts.part_id,infinera.parts.part_name,infinera.parts.material_number,"\
                " infinera.`part cost ID`.standard_cost,infinera.parts.part_number,"\
                "infinera.parts.part_reliability_class,infinera.parts.spared_attribute"\
                " from infinera.parts inner join infinera.`part cost ID` on infinera.parts.part_id=infinera.`part cost ID`.part_id"

        result = get_df_from_sql_query(
            query=query,
            db_connection_string=Configuration.INFINERA_DB_URL)

        result = result.loc[:, ~result.columns.duplicated()]
        #Removes duplicate column names not column values
        response = json.loads(result.to_json(orient="records", date_format='iso'))
        return response



class GetHighSpare(Resource):

    def get(self):
        query = "select t1.part_name as ClassicPON, t2.part_name as SubstitutionPON, t.given_spare_part_id, t.high_spare_part_id " \
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


class GetNode(Resource):

    def get(self):
        query = "SELECT infinera.node.node_id,infinera.node.node_name,infinera.node.end_customer_node_belongs,infinera.node.node_depot_belongs FROM infinera.node"

        result = get_df_from_sql_query(
            query=query,
            db_connection_string=Configuration.INFINERA_DB_URL)

        result = result.loc[:, ~result.columns.duplicated()]
        #Removes duplicate column names not column values
        response = json.loads(result.to_json(orient="records", date_format='iso'))
        return response


class GetDepot(Resource):

    def get(self):
        query = "SELECT depot_id,depot_name,depot_address,city,state,country,region,hub,partner,partner_warehouse_code,contact,lat,infinera.depot.long FROM infinera.depot"

        result = get_df_from_sql_query(
            query=query,
            db_connection_string=Configuration.INFINERA_DB_URL)

        result = result.loc[:, ~result.columns.duplicated()]
        #Removes duplicate column names not column values
        response = json.loads(result.to_json(orient="records", date_format='iso'))
        return response


class GetMisnomer(Resource):

    def get(self):
        query = "select t1.part_name as CorrectPON, t.misnomer_pon_name as MisnomerPON, t.reference_tabel_id,t1.part_id "\
                " from infinera.`Misnomer PON Conversion` t"\
                " inner join infinera.parts t1 on t1.part_id = t.correct_part_id"
        result = get_df_from_sql_query(
            query=query,
            db_connection_string=Configuration.INFINERA_DB_URL)

        result = result.loc[:, ~result.columns.duplicated()]
        #Removes duplicate column names not column values
        response = json.loads(result.to_json(orient="records", date_format='iso'))
        return response