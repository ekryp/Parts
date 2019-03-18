FROM ubuntu:16.04
FROM python:3.5
COPY . /code/
COPY entrypoint.sh /
RUN mkdir /data
WORKDIR /code
RUN pip install -r requirements.txt
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "vim"]
ENTRYPOINT /entrypoint.sh
