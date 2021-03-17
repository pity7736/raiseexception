#!/usr/bin/env bash
docker-compose run --rm -e APP_ENVIRONMENT=testing raise_exception pytest -s -vvv --cov=raiseexception --cov-report term-missing tests
