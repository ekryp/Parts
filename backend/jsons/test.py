import  json
f = open("incident.json")
data = json.load(f)
print(data['spec']['ioConfig']['inputSpec']['paths'])
print(data['spec']['dataSchema']['dataSource'])

data['spec']['ioConfig']['inputSpec']['paths']="/path/incident_2000"
data['spec']['dataSchema']['dataSource'] = "incident_2000"

with open('data.json', 'w') as fp:
    json.dump(data, fp,indent=4)