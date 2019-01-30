#!/usr/bin/bash

# change directory to backend directory
cd /home/aashish/Parts/backend

#activate virtualenv
source env/bin/activate

pip3.5 install -r requirements.txt

#kill backend services if running
kill -9 $(ps -eaf | grep -i startserver | grep -v 'grep' | awk '{print $2}') &> /dev/null

if [ $? != 0 ]
then
       echo "Backend Services not running & starting backend services,creating logs in backend_nohup.out file"
fi

kill -9 $(ps -eaf | grep -i gunicorn | grep -v 'grep' | awk '{print $2}') &> /dev/null

if [ $? != 0 ]
then
       echo "Backend Services not running & starting backend services,creating logs in backend_nohup.out file"
fi


#start backend services
nohup gunicorn app:app -w 4 --log-level debug -b 0.0.0.0:5000 --timeout 600 > backend.log&

#kill celery  if running
kill -9 $(ps -eaf | grep -i celery | grep -v 'grep' | awk '{print $2}') &> /dev/null
if [ $? != 0 ]
then
       echo "Celery Services not running & starting Celery services,creating logs in celery.log file"
fi
#start celery

#sudo rabbitmq-server start
celery -A app.tasks:celery worker --concurrency=1 > celery.log&
