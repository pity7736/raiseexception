from starlette.applications import Starlette
from starlette.routing import Route, Mount

from raiseexception import settings
from raiseexception.auth.views import auth_views


def index(request):
    return settings.TEMPLATE.TemplateResponse(
        'index.html',
        {'request': request}
    )


routes = [
    Route('/', index),
    Mount('/auth', routes=auth_views.routes)
]

if settings.APP_ENVIRONMENT == 'dev':
    from starlette.staticfiles import StaticFiles
    routes.extend((
        Mount(
            '/static',
            app=StaticFiles(directory=settings.STATIC_DIR),
            name='static'
        ),
        Mount(
            '/media',
            app=StaticFiles(directory=settings.MEDIA_DIR),
            name='media'
        )
    ))

app = Starlette(debug=settings.DEBUG, routes=routes)
