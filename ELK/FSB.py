from tika import parser
import time
from itertools import zip_longest
from collections import defaultdict
import requests
import os
import shutil
import glob
import sys


os.chdir(r'/Users/anup/Downloads/FSB')

for each_pdf in ['FSB_180813-A.pdf']:
    # read input file
    print(each_pdf)
    raw = parser.from_file(each_pdf)
    raw = raw.get('content')
    str_list = raw.split('\n\n')
    result = list(filter(None, str_list))

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
    result = result[start_index:end_index]
    print(result)


    def predicate_grouper(li, predicate='Issue #'):
        indices = [i for i, x in enumerate(result) if x.startswith(predicate)]
        slices = [slice(*x) for x in zip_longest(indices, indices[1:])]
        for sli in slices:
            yield ' '.join(li[sli])


    result = (list(predicate_grouper(result)))

    for each_issue in result:
        dd = defaultdict(dict)
        dd['Issue Id'] = each_issue.split('Problem Description')[0].split(':')[0].split('#')[1]
        dd['Issue Title'] = each_issue.split('Problem Description')[0].split(':')[1]
        dd['Problem Description'] = each_issue.split('Problem Description')[1].split('Symptoms')[0]
        dd['Symptoms'] = each_issue.split('Problem Description')[1].split('Symptoms')[1].split('Root Cause')[0]
        dd['Root Cause'] = each_issue.split('Problem Description')[1].split('Symptoms')[1].split('Root Cause')[1]
        print('=' * 70)
        print(dd)
        print('=' * 70)