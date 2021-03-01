import os

from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates

from raiseexception import settings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = f'{BASE_DIR}/templates'
templates = Jinja2Templates(directory=TEMPLATE_DIR)


def index(request):
    return templates.TemplateResponse('index.html', {'request': request})


routes = [
    Route('/', index),
]

if settings.APP_ENVIRONMENT == 'dev':
    from starlette.staticfiles import StaticFiles
    routes.extend((
        Mount(
            '/static',
            app=StaticFiles(directory=f'{TEMPLATE_DIR}/static'), name='static'
        ),
        Mount(
            '/media',
            app=StaticFiles(directory=f'{TEMPLATE_DIR}/media'), name='media'
        )
    ))

app = Starlette(debug=settings.DEBUG, routes=routes)
