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


os.chdir(r'/tmp')

for each_doc in glob.glob("*.docx"):

    # read input file
    print(each_doc)
    raw = parser.from_file(each_doc)
    raw = raw.get('content')
    str_list = raw.split('\n')
    result = list(filter(None, str_list))

    final_items = []
    start_points = []

    # Get index of all Objective word in list
    for ix, item in enumerate(result):
        if 'Objective'.lower() in item.lower():
            start_points.append(ix)

for idx, value in enumerate(start_points):
    try:
        # To get each record we get data in between 2 Objective word & save in new list of record as final items
        thiselem = value
        nextelem = start_points[(idx + 1) % len(start_points)]
        final_items.append(result[thiselem:nextelem])

    except:
        pass
# iterate over each record to get respective key value pair in records
# like Objective,Procedures, Expected Results
for each_record in final_items:
    is_objective = False
    is_procedure = False
    is_result = False
    dd = defaultdict(dict)
    size=len(each_record)

    for index, item in enumerate(each_record):

        if 'Objective'.lower() in item.lower():
            is_objective = True
            objective_index = index

        if is_objective and 'Procedure'.lower() in item.lower():
            is_procedure = True
            procedure_index = index

        if 'Expected Result'.lower() in item.lower():
            is_result = True
            result_index = index

        if (index + 1) == size:
            try:
                dd['file_name'] = each_doc
                # If record field does not have Expected Result, we capture procedure till end
                if not is_result:
                    dd['Objective'] = each_record[objective_index + 1]
                    dd['Procedure'] = each_record[procedure_index + 1:]
                    print(dd)
                    break
                # If record field  have Expected Result, we capture procedure till start of Expected Result
                elif is_result:
                    dd['Objective'] = each_record[objective_index + 1]
                    dd['Procedure'] = each_record[procedure_index + 1:result_index]
                    print(dd)
            except:
                break





    '''
    
    def predicate_grouper(li, predicate='Objective'):
        indices = [i for i, x in enumerate(result) if x.startswith(predicate)]
        slices = [slice(*x) for x in zip_longest(indices, indices[1:])]
        for sli in slices:
            yield ' '.join(li[sli])


    result = (list(predicate_grouper(result)))
    for item in result:
        print('#' * 50)
        print(item)
        print('#' * 50)
    '''
