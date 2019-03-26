FROM python:3.5
RUN apt-get update -y
RUN apt-get install -y vim
COPY requirements.txt /code/
COPY entrypoint.sh /
RUN mkdir /data
WORKDIR /code
RUN pip install -r requirements.txt
ENTRYPOINT /entrypoint.sh
