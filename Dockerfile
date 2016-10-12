FROM python:2.7.11
MAINTAINER Antonis Kalipetis <akalipetis@sourcelair.com>

RUN apt-get update &&\
    apt-get install -y netcat && \
    mkdir -p /usr/src/app && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /usr/src/app

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app
