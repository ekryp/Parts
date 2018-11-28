#!/usr/bin/env python
import os, sys
from flask_script import Manager, Shell, Server
from app import app
from app.models.basemodel import db
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)
# access python shell with context
manager.add_command(
    "shell",
    Shell(make_context=lambda: {'app': app, 'db': db}), use_ipython=True)

# run the app
manager.add_command(
    "startserver",
    Server(port=(os.getenv('FLASK_PORT') or 5000), host='0.0.0.0', threaded=True))

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	if sys.version_info.major < 3:
		current_version = '.'.join(str(x) for x in sys.version_info[:3])
		raise ImportError('Python version 3 or Higher required. Current version: %s' % current_version)
	manager.run()

