import os

env = os.getenv('EKRYP_ENV', 'prod')

if env == 'prod':
	from .prod_config import Configuration
elif env == 'uat':
	from .uat_config import Configuration
else:
	from .dev_config import Configuration

Configuration.SQLALCHEMY_DATABASE_URI = Configuration.EKRYP_USER_DB_URI
print("{}\n`{}` Configuration loaded.\n{}".format('-'*40, env, '-'*40))
