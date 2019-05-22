import os
from tika import parser
import requests
import config
from requests.auth import HTTPBasicAuth
from collections import defaultdict
from datetime import date

pdfs = []

# Get pdf files with full file path in given directory
for parent, dirnames, filenames in os.walk('/Users/anup/Downloads/MOP'):
    for fn in filenames:
        if fn.lower().endswith('.pdf'):
            pdfs.append(os.path.join(parent, fn))

for each_pdf in pdfs:
    print(each_pdf)
    raw = parser.from_file(each_pdf)
    raw = raw.get('content')

    str_list = raw.split('\n')
    result = list(filter(None, str_list))

    # Get Title from result list
    # It present after METHOD OF PROCEDURE (MOP) line & before Rev. Line

    for item in result:
        if 'MOP' in item:
            start = result.index(item)
            break

    for item in result:
        if 'Rev.' in item:
            end = result.index(item)
            break

    title = result[start +1 :end]
    # remove empty lines
    title = [x for x in title if not x.isspace()]

    # join non-empty rows to one
    title = ''.join(title)
    print(title)

    # Get Introduction from result list
    # It starts with Introduction line & before Requirements and Pre-Requisites Line

    for item in result:
        if 'Introduction' in item:
            start = result.index(item)
            break
    for item in result:
        if 'Requirements and Pre-Requisites' in item:
            end = result.index(item)
            break

    Introduction = result[start + 1:end]
    # remove empty lines
    Introduction = [x for x in Introduction if not x.isspace()]

    # join non-empty rows to one
    Introduction = ''.join(Introduction)
    print(Introduction)

    dd = defaultdict(dict)
    dd['timestamp'] = date.today().isoformat()
    dd['title'] = title
    dd['introduction'] = Introduction
    dd['file_name'] = os.path.split(each_pdf)[1]
    response = requests.post(config.ELK_URI + "mop/_doc", json=dd,
                             auth=HTTPBasicAuth(config.ELK_USERNAME, config.ELK_PASSWORD),
                             headers={"content-type": "application/json"})






