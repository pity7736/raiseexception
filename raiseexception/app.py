import os

from starlette.applications import Starlette
from starlette.routing import Route
from starlette.templating import Jinja2Templates

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=f'{BASE_DIR}/templates/')


def index(request):
    return templates.TemplateResponse('index.html', {'request': request})


routes = (
    Route('/', index),
)

app = Starlette(debug=True, routes=routes)
