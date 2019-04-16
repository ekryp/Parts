From python:3.5
COPY . /code/
COPY entrypoint.sh /
WORKDIR /code
RUN pip install -r requirements.txt
ENTRYPOINT /entrypoint.sh
