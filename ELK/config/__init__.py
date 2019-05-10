import os

env = os.getenv('EKRYP_ENV', 'uat')

if env == 'prod':
	ELK_URI = ""
elif env == 'uat':
	ELK_URI = "https://59a139b294d44d1daf54ef37b0820bb5.us-west-2.aws.found.io:9243/"
	ELK_USERNAME = "elastic"
	ELK_PASSWORD = "eC7dPhDPYNICVSkzXa1QFXcw"