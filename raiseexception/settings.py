import os

from starlette.templating import Jinja2Templates

# application
APP_ENVIRONMENT = os.environ['APP_ENVIRONMENT']
DEBUG = APP_ENVIRONMENT == 'dev'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# database
DB_HOST = os.environ['KINTON_HOST']
DB_USER = os.environ['KINTON_USER']
DB_NAME = os.environ['KINTON_DATABASE']
DB_PASSWORD = os.environ['KINTON_PASSWORD']
DB_PORT = os.environ['KINTON_PORT']

# crypto
UNKNOWN_PASSWORD_WORD = os.environ['UNKNOWN_PASSWORD_WORD']
SESSION_TOKEN_LENGTH = 64

# html
TEMPLATE_DIRS = f'{BASE_DIR}/templates'
TEMPLATE = Jinja2Templates(directory=TEMPLATE_DIRS)
STATIC_DIR = f'{TEMPLATE_DIRS}/static'
MEDIA_DIR = f'{TEMPLATE_DIRS}/media'
