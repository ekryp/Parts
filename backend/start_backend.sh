#!/usr/bin/bash

# change directory to backend directory
cd /home/attachedDisk/eKrypFeeder/backend

#activate virtualenv
source env/bin/activate

#kill backend services if running
kill $(ps -eaf | grep -i "python manage.py startserver" | grep -v "grep" | awk '{print $2}') &> /dev/null

if [ $? != 0 ]
then
       echo "Backend Services not running & starting backend services,creating logs in backend_nohup.out file"
fi

#start backend services
nohup python manage.py startserver > backend.log&

#kill celery  if running
kill $(ps -eaf | grep -i "celery -A app.tasks:celery worker --concurrency=1" | grep -v "grep" | awk '{print $2}') &> /dev/null
if [ $? != 0 ]
then
       echo "Celery Services not running & starting Celery services,creating logs in celery.log file"
fi
#start celery

#sudo rabbitmq-server start
celery -A app.tasks:celery worker --concurrency=1 > celery.log&