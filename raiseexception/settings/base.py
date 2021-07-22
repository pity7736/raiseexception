import os

from starlette.templating import Jinja2Templates

# application
APP_ENVIRONMENT = os.environ['APP_ENVIRONMENT']
DEBUG = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# database
DB_HOST = os.environ['KINTON_HOST']
DB_USER = os.environ['KINTON_USER']
DB_NAME = os.environ['KINTON_DATABASE']
DB_PASSWORD = os.environ['KINTON_PASSWORD']
DB_PORT = os.environ['KINTON_PORT']

# crypto
SESSION_TOKEN_LENGTH = 64
SESSION_COOKIE_NAME = '__Secure-raiseexception-session'

# html
TEMPLATE_DIRS = f'{BASE_DIR}/templates'
TEMPLATE = Jinja2Templates(directory=TEMPLATE_DIRS)
STATIC_DIR = f'{TEMPLATE_DIRS}/static'
MEDIA_DIR = f'{TEMPLATE_DIRS}/media'

# mailing
ADMIN_EMAIL = os.environ['ADMIN_EMAIL']
MAIL_USERNAME = os.environ['MAIL_USERNAME']
MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
MAIL_SANDBOX = False
