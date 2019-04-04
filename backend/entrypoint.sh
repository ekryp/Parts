#!/bin/sh
python -u  manage.py startserver 2>&1 >/python.log & tail -f /python.log & celery -A app.tasks:celery worker --concurrency=1