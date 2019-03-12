import requests
from flask_restful import Resource
from flask_restful import reqparse
from flask import jsonify
from bs4 import BeautifulSoup
import json
import os 
import re

class MailGun(Resource):

    def __init__(self):
         self.reqparse = reqparse.RequestParser()
         self.reqparse.add_argument('senderEmailAddress', type=str, required=True, location='json')
         self.reqparse.add_argument('recevierEmailAddress', type=str, required=True, location='json')
         self.reqparse.add_argument('emailSubject', type=str, required=True, location='json')
         self.reqparse.add_argument('emailMessage', type=str, required=True, location='json')
         super(MailGun, self).__init__()
        
    def post(self):
        args = self.reqparse.parse_args()
        print('entering the mail method',args)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        print("dirpath ------>",dir_path)
        htmlFile = dir_path+'/EmailTemplate.html'
        content = open(htmlFile, "r").read()
        soup = BeautifulSoup(content)
        target = soup.find_all(text=re.compile(r'ekrypmessage'))
        for v in target:
            v.replace_with(v.replace('ekrypmessage',args['emailMessage']))
        response = requests.post("https://api.mailgun.net/v3/noreply.ekryp.com/messages",
                             auth=("api","key-06a2334ec7daa13d562564d303582d63"),
                             data={"from": args['senderEmailAddress'],
                                    "to": args['recevierEmailAddress'],
                                    "subject" :args['emailSubject'],
                                    "html": soup,
                                    "subscribed": True})
        emailResponse = json.loads(response.content.decode("utf-8"))
        print(emailResponse)
        return jsonify(msg=emailResponse['message'], http_status_code=200)



