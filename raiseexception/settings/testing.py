from .base import *  # noqa: F401, F403

APP_DOMAIN = 'testserver.local'
DB_NAME += '_test'  # noqa: F405
MAIL_SANDBOX = True
SITE = f'http://{APP_DOMAIN}'
