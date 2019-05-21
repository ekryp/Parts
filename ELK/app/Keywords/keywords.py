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
            keyword_df = pd.read_excel('Key Words.xlsx', header=None)
            keywords = keyword_df[0].tolist()

            # get keywords from input
            found_keyword = []
            for keyword in keywords:
                if keyword.lower() in input_:
                    if keyword not in found_keyword:
                        found_keyword.append(keyword)

            print("Keywords found in input are {0}".format(found_keyword))

            # get problem area from keywords
            problem_area_df = pd.read_excel('UI_Elastic.xlsx')
            found_problem_area = []

            for keyword in found_keyword:
                matched_problem_area = problem_area_df[problem_area_df['Key Words'].str.match(keyword, case=False)]

                if not matched_problem_area.empty:
                    for each_problem_area in matched_problem_area['UI Problem Area Map'].tolist():
                        if each_problem_area not in found_problem_area:
                            found_problem_area.append(each_problem_area)

            print("Problem Area found are {0}".format(found_problem_area))

            # Get elastic search words
            elastic_search_df = pd.read_excel('Keyword_UI.xlsx')
            found_elastic_search_words = []

            for problem_area in found_problem_area:
                matched_elastic_search_words = elastic_search_df[elastic_search_df['UI Problem Area Map'].str.match(problem_area, case=False)]

                if not matched_elastic_search_words.empty:
                    for each_elastic_word in matched_elastic_search_words['Elastic Search Map'].tolist():
                        if each_elastic_word not in found_elastic_search_words:
                            found_elastic_search_words.append(each_elastic_word)

            print("elastic search words found are {0}".format(found_elastic_search_words))

            return jsonify(ml_keywords=found_problem_area,  ml_synonym=found_elastic_search_words, http_status_code=200)
