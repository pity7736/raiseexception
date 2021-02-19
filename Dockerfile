FROM python:3.9 AS base

ENV PYTHONUNBUFFERED=1
ENV CODE=/code
WORKDIR $CODE

COPY requirements.txt .
RUN apt-get update && apt-get -y upgrade
RUN pip install -r requirements.txt


FROM base AS testing

COPY requirements_dev.txt .
RUN pip install -r requirements_dev.txt


FROM base AS web
COPY . $CODE
