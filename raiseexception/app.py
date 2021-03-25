import asyncio

from kinton.utils import get_connection
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.routing import Route, Mount

from raiseexception import settings
from raiseexception.admin.views import admin_views
from raiseexception.auth.controllers import CookieAuthBackend
from raiseexception.auth.views import auth_views
from raiseexception.blog.views import blog_views


def index(request):
    return settings.TEMPLATE.TemplateResponse(
        'index.html',
        {'request': request}
    )


routes = [
    Route('/', index),
    Mount('/auth', routes=auth_views.routes, name='auth'),
    Mount('/admin', routes=admin_views.routes, name='admin'),
    Mount('/blog', routes=blog_views.routes, name='blog')
]

if settings.DEBUG:
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


async def _initialize_db(attempt=1):
    sql_file = f'{settings.BASE_DIR}/../tests/integration_tests/db.sql'
    with open(sql_file) as f:
        sql = f.read()

    try:
        connection = await get_connection()
    except (ConnectionResetError, ConnectionRefusedError):
        print('connection error')
        if attempt < 4:
            print(f'sleeping {attempt} seconds')
            await asyncio.sleep(attempt)
            print('retrying...')
            return await _initialize_db(attempt + 1)
    else:
        await connection.execute(sql)


app = Starlette(
    debug=settings.DEBUG,
    routes=routes,
    on_startup=[_initialize_db],
    middleware=(
        Middleware(AuthenticationMiddleware, backend=CookieAuthBackend()),
    )
)
