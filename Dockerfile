FROM python:3.8
MAINTAINER TihomirGalov

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y gettext

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /code
WORKDIR /code
COPY . /code
