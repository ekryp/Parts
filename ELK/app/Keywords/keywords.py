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
            df = pd.read_excel('Keyword_UI.xlsx')
            df_e = pd.read_excel('UI_Elastic.xlsx')

            df[df.columns[1]] = df[df.columns[1]].astype(str)
            df[df.columns[0]] = ' ' + df[df.columns[0]].astype(str) + ' '
            df[df.columns[0]] = df[df.columns[0]].str.lower()
            list_keywords = list(df[df.columns[0]])
            list_tags = list(df[df.columns[1]])

            list_UI_tags = list(df_e[df_e.columns[0]])
            list_elastic = list(df_e[df_e.columns[1]])

            def check(word):
                if word in input_:
                    return True
                return False

            ans = ""
            set_ = set()
            for ind, val in enumerate(list_keywords):
                if check(val) and list_tags[ind] not in set_:
                    set_.add(list_tags[ind])
                    ans = ans + list_tags[ind] + ','

            ans_split = ans.split(',')
            ans_e = []
            for ind, val in enumerate(list_UI_tags):
                if val in ans_split:
                    ans_e.append(list_elastic[ind])

            return jsonify(ml_keywords=ans_e, ml_synonym=ans_split[:-1], http_status_code=200)
