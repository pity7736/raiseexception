FROM python:3.9 AS raiseexception_base

ENV PYTHONUNBUFFERED=1
ENV CODE=/code
WORKDIR $CODE

COPY requirements.txt .
COPY .env .
RUN apt-get update && apt-get -y upgrade


FROM raiseexception_base AS raiseexception_testing

COPY requirements_dev.txt .
RUN pip install -r requirements_dev.txt


FROM raiseexception_base AS raiseexception_web
RUN pip install -r requirements.txt
