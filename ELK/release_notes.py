from tika import parser
import time
from itertools import zip_longest
from collections import defaultdict
import requests
import os
import shutil
import glob
import sys


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
    for item in result:
        if 'Issue' in item:
            index = result.index(item)
            break
    result = result[index:]

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
                dd['Issue ID'] = r.split(':')[1]
        except:
            dd['Issue ID'] = ''
        try:
            if 'Severity' in g:
                dd['Severity'] = g.split(':')[1]
        except:
            dd['Severity'] = ''
        try:
            if 'Description' in b:
                dd['Description'] = b.split(':')[1]
        except:
            dd['Description'] = ''

        try:
            if 'Workaround' in t:
                dd['Workaround'] = t.split(':')[1]
        except:
            dd['Workaround'] = ''
        dd['file_name'] = each_pdf
        print(dd)
        response = requests.post("http://34.83.90.206:9200/infinera/release_notes/", json=dd,
                                headers={"content-type": "application/json"})
    #print(each_pdf)
    #print("sleep for 5 sec")
    shutil.move(each_pdf, r'/Users/anup/Downloads/Release_Notes/processed')
    time.sleep(5)





