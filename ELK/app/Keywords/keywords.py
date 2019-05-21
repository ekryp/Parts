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
            ml_keywords = []
            ml_synonym = []

            # Read keywords
            df1 = pd.read_excel('Keyword_UI.xlsx')
            # df2 = pd.read_excel('UI_Elastic.xlsx')

            for word in input_.split():

                df3 = df1[df1.apply(lambda row: row.astype(str).str.contains(word, case=False).any(), axis=1)]
                # df4 = df2[df2.apply(lambda row: row.astype(str).str.contains(word, case=False).any(), axis=1)]

                for matches in df3['Elastic Search Map'].tolist():
                    matches = matches.split(",")
                    for match in matches:
                        if match not in ml_synonym:
                            ml_synonym.append(match)

                for matches in df3['UI Problem Area Map'].tolist():
                    matches = matches.split(",")
                    for match in matches:
                        if match not in ml_keywords:
                            ml_keywords.append(match)

            return jsonify(ml_keywords=ml_keywords,  ml_synonym=ml_synonym, http_status_code=200)
