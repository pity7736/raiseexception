#!/usr/bin/env bash

docker-compose -f docker-compose-production.yml -f docker-compose.yml run --rm raise_exception  pytest -s -vvv --cov=raiseexception --cov-report term-missing tests
