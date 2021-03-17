#!/usr/bin/env bash

docker-compose run --rm raise_exception pytest -s -vvv --cov=raiseexception --cov-report term-missing tests
