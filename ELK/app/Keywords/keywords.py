from flask import jsonify
from flask import request
import requests
from flask_restful import Resource
from flask_restful import reqparse


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

            def check(word):
                if word in input_:
                    return True
                return False

            keywords = ["DOA", "Dead On Arrival", "Safeboot", "USB-11", "IKE", "Equipment Degrade Alarm", "Timeout",
                        "Interface Flap", "Upgrade Failed",
                        "CPUR", "Control Plane UnReachable", "MACSEC", "LOSYNC", "OLOS", "LOS", "Cold Reboot",
                        "Cold Reset", "Warm Reboot",
                        "Warm Reset", "Post-FEC BER", "Loss of Connectivity", "Low Voltage", "PIC Init State",
                        "Fatal Error", "FEC Error",
                        "Broken", "Critical Alarm", "TOM issue", "False Rx Reading", "False Tx reading", "False Alarm",
                        "BPOSTFAIL", "IGCC Failure", "DNA Lost Communication"]
            keywords = [i.lower() for i in keywords]

            desc_split = input_.split()
            ans = ""
            category =[]
            if 'rma' in desc_split or 'rmas' in desc_split:
                ans = ans + 'RMA' + ','
                category.append('RMA')
            if 'service return' in input_:
                ans = ans + 'Service Return' + ','
                category.append('Service Return')
            if 'refurbish' in desc_split or 'move the unit to ufg' in input_:
                ans = ans + 'ECO/Refurbish' + ','
                category.append('ECO/Refurbish')
            if check('replace and upgrade') or check('defective'):
                ans = ans + 'Replace/Upgrade' + ','
                category.append('Replace/Upgrade')
            if check('equipment failure') or check('equipment fail') or check('equipment failur') or (
                check('faulty') and check('equipment')):
                ans = ans + 'Faulty Equipment' + ','
                category.append('Faulty Equipment')
            if check('scrap'):
                ans = ans + 'Scrap' + ','
                category.append('Scrap')
            if check('traffic hit') or check('dropping traffic') or check('network outage') or check('outage') or check(
                    'traffic glitch') or check('disruption in service'):
                ans = ans + 'Network Down' + ','
                category.append('Network Down')
            if check('continuous reboot') or check('reboot loop'):
                ans = ans + 'Reboot Loop' + ','
                category.append('Reboot Loop')
            for x in keywords:
                if check(x):
                    ans = ans + x + ','
                    category.append(x)

            #return ans
            return jsonify(ml_kewords=category, http_status_code=200)
