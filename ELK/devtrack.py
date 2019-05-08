import csv, json
import requests
from requests.auth import HTTPBasicAuth 
import config


def csvParse():
    # Open the CSV
    f = open( '/Users/khalisarankannan/Downloads/elktest.csv', 'rU' )
        # Change each fieldname to the appropriate field name. 
    reader = csv.DictReader( f, fieldnames = ( "Issue ID","Title","Type","Current Owner",
     "Progress Status", "Group", "Severity", "Date Submitted", "Submitted By", "Description",
      "Found in Build", "Target Release", "Date Closed", "HW PON","Case Reason",
      "Final Test Root Cause Analysis Comments","Priority","Found on Platform","Product",
      "Problem Description/Systems Impacted","Workaround","Symptoms","Reporting Customer",
      "Service Account","Fixed in Release","Found in Release","Resolution"))
    issueId = []
    store = []
    for row in reader:
        frame = {"issueId":row["Issue ID"].replace(u'\xa0', u''), 
        "title": row["Title"].replace(u'\xa0', u''),
        "type": row["Type"].replace(u'\xa0', u''),
        "currentOwner":row['Current Owner'].replace(u'\xa0', u''),
        "progressStatus": row["Progress Status"].replace(u'\xa0', u''),
        "group": row["Group"].replace(u'\xa0', u''),
        "severity":row['Severity'].replace(u'\xa0', u''),
        "dateSubmitted": row["Date Submitted"].replace(u'\xa0', u''),
        "submittedBy": row["Submitted By"].replace(u'\xa0', u''),
        "description":row['Description'].replace(u'\xa0', u''),
        "foundInBuild": row["Found in Build"].replace(u'\xa0', u''),
        "tragetRelease": row["Target Release"].replace(u'\xa0', u''),
        "dateClosed":row['Date Closed'].replace(u'\xa0', u''),
        "hwPON": row["HW PON"].replace(u'\xa0', u''),
        "caseReason": row["Case Reason"].replace(u'\xa0', u''),
        "finalTestRootCauseAnalysisComments":row['Final Test Root Cause Analysis Comments'].replace(u'\xa0', u''),
        "priority": row["Priority"].replace(u'\xa0', u''),
        "foundOnPlatform": row["Found on Platform"].replace(u'\xa0', u''),
        "product":row['Product'].replace(u'\xa0', u''),
        "problemDescriptionImpacted": row["Problem Description/Systems Impacted"].replace(u'\xa0', u''),
        "workaround": row["Workaround"].replace(u'\xa0', u''),
        "symptoms":row['Symptoms'].replace(u'\xa0', u''),
        "reportingCustomer": row["Reporting Customer"].replace(u'\xa0', u''),
        "serviceAccount": row["Service Account"].replace(u'\xa0', u''),
        "fixedinRelease":row['Fixed in Release'].replace(u'\xa0', u''),
        "foundinRelease":row['Found in Release'].replace(u'\xa0', u''),
        "resolution":row['Resolution'].replace(u'\xa0', u'')
        }
        if row["Issue ID"] not in issueId:
            issueId.append(row["Issue ID"])
            store.append(frame)
   
    # Parse the CSV into JSON
    out = json.dumps(store, indent=4)
    orginalJSON = json.loads(out)
    orginalJSON.pop(0)
    data = orginalJSON

    for doc in data:
        doc["id"]= doc["issueId"]
        response = requests.post(config.ELK_URI+"devtrack/_doc/"+doc["issueId"],auth=HTTPBasicAuth(config.ELK_USERNAME,config.ELK_PASSWORD),json=doc,headers={"content-type":"application/json"})
        print('ELK response ----->',response.content)

csvParse()