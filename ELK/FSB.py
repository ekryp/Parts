from tika import parser
import time
from itertools import zip_longest
from collections import defaultdict
import requests
import os
import shutil
import glob
import sys
from requests.auth import HTTPBasicAuth 
from datetime import date, timezone
import config


os.chdir(r'/Users/khalisarankannan/Downloads/fsb')

for each_pdf in glob.glob("*.pdf"):

    # read input file
    print(each_pdf)
    raw = parser.from_file(each_pdf)
    raw = raw.get('content')
    str_list = raw.split('\n\n')
    result = list(filter(None, str_list))
    field_service_bulletin = []

    # Take records from Field Service Bulletin only
    for item in result:
        if 'FSB Number' in item:
            start = result.index(item)
            break

    # Take records till Synopsis only
    for item in result:
        if 'Synopsis' in item:
            end = result.index(item)
            break

    try:
        field_service_bulletin = result[start:end]
        print(field_service_bulletin)
    except NameError:
        print("cant find either FSB Number #  or Synopsis in pdf {0}".format(each_pdf))
        shutil.move(each_pdf, r'/Users/khalisarankannan/Downloads/fsb/failed')
        continue

    common_attribute = defaultdict(dict)
    for item in field_service_bulletin:
        if 'FSB Number' in item:
            common_attribute['FSBNumber'] = item.split('FSB Number')[1]
            print("item in FSB Number is {0}".format(common_attribute.get('FSBNumber')))

        elif 'FSB Title' in item:
            common_attribute['title'] = item.split('FSB Title')[1]
            print("item in FSB Title is {0}".format(common_attribute.get('title')))

        elif 'Date Created' in item:
            common_attribute['dateCreated'] = item.split('Date Created')[1]
            print("item in Date Created is {0}".format(common_attribute.get('dateCreated')))

        elif 'Date Revised' in item:
            common_attribute['dateRevised'] = item.split('Date Revised')[1]
            print("item in Date Revised is {0}".format(common_attribute.get('dateRevised')))



    # Take records from Issue # only
    for item in result:
        if 'Issue #' in item:
            start_index = result.index(item)
            break


    # Take records till Recommended Actions only
    for item in result:
        if 'Recommended Actions' in item:
            end_index = result.index(item)
            break

    try:
        result = result[start_index:end_index]
        print(result)
    except NameError:
        print("Cant find either Issue #  or Recommended Actions in pdf {0}".format(each_pdf))
        shutil.move(each_pdf, r'/Users/khalisarankannan/Downloads/fsb//failed')
        continue


    def predicate_grouper(li, predicate='Issue #'):
        indices = [i for i, x in enumerate(result) if x.startswith(predicate)]
        slices = [slice(*x) for x in zip_longest(indices, indices[1:])]
        for sli in slices:
            yield ' '.join(li[sli])


    result = (list(predicate_grouper(result)))

    for each_issue in result:
        dd = defaultdict(dict)
        dd['issueId'] = each_issue.split('Problem Description')[0].split(':')[0].split('#')[1]
        dd['title'] = each_issue.split('Problem Description')[0].split(':')[1]
        dd['description'] = each_issue.split('Problem Description')[1].split('Symptoms')[0]
        dd['symptoms'] = each_issue.split('Problem Description')[1].split('Symptoms')[1].split('Root Cause')[0]
        dd['rootCause'] = each_issue.split('Problem Description')[1].split('Symptoms')[1].split('Root Cause')[1]
        dd['file_name'] = each_pdf
        dd['timestamp'] = date.today().isoformat()
        print('=' * 70)
        dd.update(common_attribute)
        print(dd)
        print('=' * 70)
        response = requests.post(config.ELK_URI+"fsb/_doc", json=dd,auth=HTTPBasicAuth(config.ELK_USERNAME,config.ELK_PASSWORD),
                                 headers={"content-type": "application/json"})

    shutil.move(each_pdf, r'/Users/khalisarankannan/Downloads/fsb/processed')
