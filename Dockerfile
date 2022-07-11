FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

RUN apk update && apk add postgresql-dev gcc  musl-dev 

WORKDIR /core

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt