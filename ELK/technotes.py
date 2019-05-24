import os
from tika import parser
import requests
import config
from requests.auth import HTTPBasicAuth
from collections import defaultdict
from datetime import date

pdfs = []

# Get pdf files with full file path in given directory
for parent, dirnames, filenames in os.walk('/Users/anup/Downloads/Tech Notes'):
    for fn in filenames:
        if fn.lower().endswith('.pdf'):
            pdfs.append(os.path.join(parent, fn))


for each_pdf in pdfs:
    print('#' * 100)
    print(each_pdf)
    raw = parser.from_file(each_pdf)
    raw = raw.get('content')

    str_list = raw.split('\n')
    result = list(filter(None, str_list))

    # Get Description from result list
    # It present after Description line
    Description = ''
    for item in result:
        if 'Description' in item:
            start = result.index(item)
            Description = result[start + 1]
            # print(Description)
            break

    # Get Release / Products Affected from result list
    # It present after Release / Products Affected line
    release_product_affected = ''
    for item in result:
        if 'Release / Products Affected' in item:
            start1 = result.index(item)
            release_product_affected = result[start1 + 1]
            # print(release_product_affected)
            break

        elif 'Affected Release / Product' in item:
            start1 = result.index(item)
            release_product_affected = result[start1 + 1]
            # print(release_product_affected)
            break

    dd = defaultdict(dict)
    dd['timestamp'] = date.today().isoformat()
    dd['description'] = Description
    dd['file_name'] = os.path.split(each_pdf)[1]
    if not release_product_affected.isspace() and release_product_affected!="":
        dd['release_product_affected'] = release_product_affected
    print(dd)
    print('#' * 100)

    response = requests.post(config.ELK_URI + "technotes/_doc", json=dd,
                             auth=HTTPBasicAuth(config.ELK_USERNAME, config.ELK_PASSWORD),
                             headers={"content-type": "application/json"})








