FROM ubuntu:jammy

RUN apt-get update -y && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
	&& localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

RUN apt-get upgrade -y && apt-get update -y

RUN apt-get install -y python3
RUN apt-get install python3-pip -y

WORKDIR /usr/src/app

COPY docker_setup/requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY docker_setup/create_sk_db.sql docker_setup/main.py docker_setup/space_kings.sqlite3 ./
COPY docker_setup/cogs/* /usr/src/app/cogs/

CMD [ "python3", "./main.py" ]
