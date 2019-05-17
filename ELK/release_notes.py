from tika import parser
import time
from itertools import zip_longest
from collections import defaultdict
import requests
import os
import shutil
import glob
import sys
from datetime import date, timezone
from requests.auth import HTTPBasicAuth 
import config
import pytz

# date = datetime.now(pytz.utc)
# print(datetime.now(timezone.utc).isoformat())

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


os.chdir(r'/Users/anup/Downloads/Release_Notes')
for each_pdf in glob.glob("*.pdf"):
    # read input file
    print(each_pdf)
    raw = parser.from_file(each_pdf)
    raw = raw.get('content')

    str_list = raw.split('\n\n')
    result = [x for x in str_list if ':' in x and ('Issue ID' in x or
                                                    'IssueID' in x or
                                                  'Severity' in x or
                                                  'Description' in x or
                                                  'Workaround' in x)]
    # Take records from issue id only
    for item in result:
        if 'Issue' in item:
            index = result.index(item)
            break
    result = result[index:]

    # Remove duplicate Description or Workaround in one record of 4
    for index, item in enumerate(result):
        print(index, item)
        if 'Description' in item:
            try:
                if 'Description' in result[index + 1]:
                    del result[index + 1]
            except:
                pass

        if 'Workaround' in item:
            try:
                if 'Workaround' in result[index + 1]:
                    del result[index + 1]
            except:
                pass

    if len(result) == 0:
        print(each_pdf)
        print("nothing")
        print("sleep for 5 sec")
        shutil.move(each_pdf, r'/Users/anup/Downloads/Release_Notes/processed')
        time.sleep(5)
        continue

    # If Workaround is not there add '' value to it ,so that we get list with sequence
    # Issue ID , Severity , Description, Workaround

    i = 0
    flag = True
    start = time.time()
    while flag:
        for r, g, b, t in grouper(result, 4):

            end = time.time()

            if end - start > 60:
                print("something wrong with pdf {0}".format(each_pdf))
                shutil.move(each_pdf, r'/Users/anup/Downloads/Release_Notes/failure')
                sys.exit(2)

            print(r, g, b, t)
            print(i)
            print(each_pdf)
            if i >= len(result):
                flag = False

            try:
                if 'Issue' not in r:
                    result.insert(i, 'Issue ID: ')
            except:
                result.insert(i, 'Issue ID: ')
            i = i + 1

            try:
                if 'Severity' not in g:
                    result.insert(i, 'Severity: ')
            except:
                result.insert(i, 'Severity: ')
            i = i + 1

            try:
                if 'Description' not in b:
                    result.insert(i, 'Description: ')
            except:
                result.insert(i, 'Description: ')

            i = i + 1

            try:
                if 'Workaround' not in t:
                    result.insert(i, 'Workaround: ')
            except:
                result.insert(i, 'Workaround: ')

            i = i + 1
            old_row = set()

            continue

    for r, g, b, t in grouper(result, 4):
        #print(r, g, b, t)
        dd = defaultdict(dict)
        try:
            if 'Issue' in r:
                dd['issueId'] = r.split(':')[1].strip()
        except:
            dd['issueId'] = ''
        try:
            if 'Severity' in g:
                dd['severity'] = g.split(':')[1].strip()
        except:
            dd['severity'] = ''
        try:
            if 'Description' in b:
                dd['description'] = b.split(':')[1].strip()
        except:
            dd['description'] = ''

        try:
            if 'Workaround' in t:
                dd['workaround'] = t.split(':')[1].strip()
        except:
            dd['workaround'] = ''
        dd['file_name'] = each_pdf
        dd['timestamp'] = date.today().isoformat()
        print(dd)
        response = requests.post(config.ELK_URI+"release_notes/_doc",auth=HTTPBasicAuth(config.ELK_USERNAME,config.ELK_PASSWORD), json=dd,
                                headers={"content-type": "application/json"})

    #print(each_pdf)
    #print("sleep for 5 sec")
    shutil.move(each_pdf, r'/Users/anup/Downloads/Release_Notes/processed')
    time.sleep(5)





