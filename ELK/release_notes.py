from tika import parser
import time
from itertools import zip_longest
from collections import defaultdict
import requests
import os
import shutil
import glob


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


os.chdir(r'/Users/anup/Downloads/Release_Notes')
for each_pdf in glob.glob("*.pdf"):
    # read input file
    print(each_pdf)
    raw = parser.from_file(each_pdf)
    raw = raw.get('content')
    str_list = raw.splitlines()
    str_list = list(filter(None, str_list))

    # keep only useful info
    search = ':'
    result = [str_list for str_list in str_list if search in str_list]
    result = [tuple(line.split(':')) for line in result]
    result = [x for x in result if len(x)==2 and ('Issue ID' in x or
                                                  'Severity' in x or
                                                  'Description' in x or
                                                  'Workaround' in x)]
    if len(result) == 0:
        print("sleep for 5 sec")
        shutil.move(each_pdf, r'/Users/anup/Downloads/Release_Notes/processed')
        time.sleep(5)
        continue

    # If Workaround is not there add '' value to it ,so that we get list with sequence
    # Issue ID , Severity , Description, Workaround

    i = 0
    flag = True
    while flag:
        for r, g, b, t in grouper(result, 4):
            if i >= len(result):
                flag = False
            i= i + 4
            try:
                if t[0] != 'Workaround':
                    result.insert(result.index(t), ('Workaround', ''))
                    break

            except:
                pass

    # group long list into seperate group of 4 Issue ID , Severity , Description, Workaround
    new_result=[]
    count=0
    for element in grouper(result, 4):

        count = count + 1
        new_result.append(element)

    # Convert group of Issue ID , Severity , Description, Workaround into dictionary
    # We cant have duplicate key in dict hence created a 2D array with unique 2d keys
    dd = defaultdict(dict)
    count = time.time()
    for item in new_result:
        dd = defaultdict(dict)
        '''
        try:
            dd[count]['Issue ID'] = item[0][1]
        except:
            dd[count]['Issue ID'] = ''
        try:
            dd[count]['Severity'] = item[1][1]
        except:
            dd[count]['Severity'] = ''
        try:
            dd[count]['Description'] = item[2][1]
        except:
            dd[count]['Description'] = ''
        try:
            dd[count]['Workaround'] = item[3][1]
        except:
            dd[count]['Workaround'] = ''
        count = count + 1
        '''
        try:
            dd['Issue ID'] = item[0][1]
        except:
            dd['Issue ID'] = ''
        try:
            dd['Severity'] = item[1][1]
        except:
            dd['Severity'] = ''
        try:
            dd['Description'] = item[2][1]
        except:
            dd['Description'] = ''
        try:
            dd['Workaround'] = item[3][1]
        except:
            dd['Workaround'] = ''
        dd['file_name'] = each_pdf

        response = requests.post("http://34.83.90.206:9200/infinera/release_notes/", json=dd,
                                 headers={"content-type": "application/json"})

    print("sleep for 5 sec")
    shutil.move(each_pdf, r'/Users/anup/Downloads/Release_Notes/processed')

    time.sleep(5)

    '''
    import json
    jj = json.dumps(dd)
    print(jj)
    '''





