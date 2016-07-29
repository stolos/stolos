FROM python:2.7.11-onbuild
MAINTAINER Antonis Kalipetis <akalipetis@sourcelair.com>

RUN apt-get update &&\
    apt-get install -y netcat
