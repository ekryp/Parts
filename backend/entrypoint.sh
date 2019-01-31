#!/bin/sh
python manage.py startserver & celery -A app.tasks:celery worker --concurrency=1
