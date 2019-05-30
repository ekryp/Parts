from requests.auth import HTTPBasicAuth
from datetime import date
from collections import defaultdict
import config
import requests

file_name = "sample_data"


def sample_data_fsb():
    dd = defaultdict(dict)
    dd['issueId'] = 7777777
    dd['title'] = "sample test fsb data"
    dd['description'] = 'I am seeing faulty  equipment degrade alarm along with "dpinit failed"  error "second string" Traffic Glitch'
    dd['timestamp'] = date.today().isoformat()
    print(dd)
    response = requests.post(config.ELK_URI + "fsb/_doc", json=dd,
                         auth=HTTPBasicAuth(config.ELK_USERNAME, config.ELK_PASSWORD),
                         headers={"content-type": "application/json"})


def sample_data_devtrack():
    dd = defaultdict(dict)
    dd['issueId'] = 7777777
    dd['title'] = "sample test devtrack data"
    dd['description'] = 'I am seeing faulty  equipment degrade alarm along with "dpinit failed"  error "second string" Traffic Glitch'
    dd['timestamp'] = date.today().isoformat()
    print(dd)
    response = requests.post(config.ELK_URI + "devtrack/_doc" + str(dd.get('issueId')), json=dd,
                         auth=HTTPBasicAuth(config.ELK_USERNAME, config.ELK_PASSWORD),
                         headers={"content-type": "application/json"})


def sample_data_release_notes():
    dd = defaultdict(dict)
    dd['issueId'] = 7777777
    dd['title'] = "sample test release_notes data"
    dd['description'] = 'I am seeing faulty  equipment degrade alarm along with "dpinit failed"  error "second string" Traffic Glitch'
    dd['timestamp'] = date.today().isoformat()
    print(dd)
    response = requests.post(config.ELK_URI + "release_notes/_doc", json=dd,
                         auth=HTTPBasicAuth(config.ELK_USERNAME, config.ELK_PASSWORD),
                         headers={"content-type": "application/json"})


def sample_data_mop():
    dd = defaultdict(dict)
    dd['issueId'] = 7777777
    dd['title'] = "sample test mop data"
    dd['introduction'] = 'I am seeing faulty  equipment degrade alarm along with "dpinit failed"  error "second string" Traffic Glitch'
    dd['timestamp'] = date.today().isoformat()
    print(dd)
    response = requests.post(config.ELK_URI + "mop/_doc", json=dd,
                         auth=HTTPBasicAuth(config.ELK_USERNAME, config.ELK_PASSWORD),
                         headers={"content-type": "application/json"})


def sample_data_testplan():
    dd = defaultdict(dict)
    dd['issueId'] = 7777777
    dd['title'] = "sample test testplan data"
    dd['Objective'] = 'I am seeing faulty  equipment degrade alarm along with "dpinit failed"  error "second string" Traffic Glitch'
    dd['timestamp'] = date.today().isoformat()
    print(dd)
    response = requests.post(config.ELK_URI + "testplan/_doc", json=dd,
                         auth=HTTPBasicAuth(config.ELK_USERNAME, config.ELK_PASSWORD),
                         headers={"content-type": "application/json"})


def sample_data_technotes():
    dd = defaultdict(dict)
    dd['issueId'] = 7777777
    dd['title'] = "sample test technotes data"
    dd['description'] = 'I am seeing faulty  equipment degrade alarm along with "dpinit failed"  error "second string" Traffic Glitch'
    dd['timestamp'] = date.today().isoformat()
    print(dd)
    response = requests.post(config.ELK_URI + "technotes/_doc", json=dd,
                         auth=HTTPBasicAuth(config.ELK_USERNAME, config.ELK_PASSWORD),
                         headers={"content-type": "application/json"})

#sample_data_fsb()
sample_data_devtrack()