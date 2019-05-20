from flask import jsonify
from flask import request
import requests
from flask_restful import Resource
from flask_restful import reqparse
import pandas as pd


class GetMLKeyWords(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('search_param', required=True, location='args')
        super(GetMLKeyWords, self).__init__()

    def get(self):
            args = self.reqparse.parse_args()
            search_param = args['search_param']
            # take input
            input_ = search_param.lower()
            print("Received Input is {0}".format(input_))

            # Read keywords
            df1 = pd.read_excel('Keyword_UI.xlsx')
            #df2 = pd.read_excel('UI_Elastic.xlsx')

            df3 = df1[df1.apply(lambda row: row.astype(str).str.contains(input_, case=False).any(), axis=1)]
            #df4 = df2[df2.apply(lambda row: row.astype(str).str.contains(input_, case=False).any(), axis=1)]
            ml_synonym = []
            for word in df3['Elastic Search Map'].tolist():
                word = word.split(",")
                ml_synonym.extend(word)

            return jsonify(ml_keywords=df3['UI Problem Area Map'].tolist(),  ml_synonym=ml_synonym, http_status_code=200)
