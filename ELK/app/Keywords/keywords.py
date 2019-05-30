from flask import jsonify
from flask import request
import requests
from flask_restful import Resource
from flask_restful import reqparse
import pandas as pd
import nltk
nltk.download('stopwords')
import re


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

            def find_double_quoted_string(text):
                # text Regex should return "String 1" or "String 2" or "String3"
                import re
                matches = re.findall(r'\"(.+?)\"', text)
                # matches is now ['String 1', 'String 2', 'String3']
                return matches
                # return ",".join(matches)
                return ', '.join(['"{}"'.format(c) for c in matches])

            one_strings = find_double_quoted_string(input_)

            # Remove one_strings from input_

            for word in one_strings:
                input_ = input_.replace(word, '')
                input_ = input_.replace('"', '')

            print("Received Input is {0}".format(input_))

            # Remove Stop words
            from nltk.corpus import stopwords
            stop = set(stopwords.words('english'))
            input = [i for i in input_.lower().split() if i not in stop]
            removed_stopwords = [i for i in input_.lower().split() if i in stop]
            input = " ".join(input)
            input = re.sub('\s+', ' ', input).strip()
            print(input)

            # Read keywords
            keyword_df = pd.read_excel('Key Words.xlsx', header=None)
            keywords = keyword_df[0].tolist()

            # get keywords from input
            def contains_word(s, w):
                return (' ' + w + ' ') in (' ' + s + ' ')

            found_keyword = []
            for keyword in keywords:
                # contains_word('the quick brown fox', 'brown')  # True
                # contains_word('the quick brown fox', 'row')    # False
                if contains_word(input_, keyword.lower()):
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
                            # remove start & end space but ont in between space in words
                            # ' one two  ' becomes 'one two'
                            each_problem_area = each_problem_area.lstrip()
                            each_problem_area = each_problem_area.rstrip()
                            found_problem_area.append(each_problem_area)

            print("Problem Area found are {0}".format(found_problem_area))

            # Get elastic search words
            elastic_search_df = pd.read_excel('Keyword_UI.xlsx')

            mapping = {}

            for problem_area in found_problem_area:
                matched_elastic_search_words = elastic_search_df[elastic_search_df['UI Problem Area Map'].str.match(problem_area, case=False)]
                found_elastic_search_words = []

                if not matched_elastic_search_words.empty:
                    for each_elastic_word in matched_elastic_search_words['Elastic Search Map'].tolist():
                        if each_elastic_word not in found_elastic_search_words:
                            # split multiple words into seperate list item
                            for each_word in each_elastic_word.split(','):
                                # remove start & end space but ont in between space in words
                                # ' one two  ' becomes 'one two'
                                each_word = each_word.lstrip()
                                each_word = each_word.rstrip()
                                found_elastic_search_words.append(each_word)

                mapping[problem_area] = found_elastic_search_words

            print("elastic search words found are {0}".format(found_elastic_search_words))

            return jsonify(mapping=mapping, input=input,
                           one_strings=one_strings, removed_stopwords=removed_stopwords, http_status_code=200)
