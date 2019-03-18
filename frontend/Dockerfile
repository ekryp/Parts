From node
COPY entrypoint.sh /
COPY . /code/
WORKDIR /code
RUN npm i
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "vim"]
ENTRYPOINT /entrypoint.sh
