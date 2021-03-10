import os


APP_ENVIRONMENT = os.environ['APP_ENVIRONMENT']
DEBUG = APP_ENVIRONMENT == 'dev'
DB_HOST = os.environ['DB_HOST']
DB_USER = os.environ['DB_USER']
DB_NAME = os.environ['DB_NAME']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_PORT = os.environ['DB_PORT']
