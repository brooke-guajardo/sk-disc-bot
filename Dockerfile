FROM ubuntu:latest

RUN apt-get update && apt-get install -y

RUN apt-get install -y python3
RUN apt-get install -y python3-pip

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY create_sk_db.sql main.py space_kings.sqlite3 ./
COPY cogs/* /usr/src/app/cogs/

CMD [ "python3", "./main.py" ]
