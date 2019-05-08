import os

env = os.getenv('EKRYP_ENV', 'uat')

if env == 'prod':
	ELK_URI = ""
elif env == 'uat':
	ELK_URI = "https://6d817865e82d41848b95cce1dd78bec0.us-east-1.aws.found.io:9243/"
	ELK_USERNAME = "elastic"
	ELK_PASSWORD = "OdKYBWWJNQEDPWD4FafW2YPE"