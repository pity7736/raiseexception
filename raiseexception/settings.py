import os


APP_ENVIRONMENT = os.environ['APP_ENVIRONMENT']
DEBUG = APP_ENVIRONMENT == 'dev'
DB_HOST = os.environ['KINTON_HOST']
DB_USER = os.environ['KINTON_USER']
DB_NAME = os.environ['KINTON_DATABASE']
DB_PASSWORD = os.environ['KINTON_PASSWORD']
DB_PORT = os.environ['KINTON_PORT']
