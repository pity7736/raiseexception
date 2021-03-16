from starlette.applications import Starlette
from starlette.routing import Route

from raiseexception import settings


def login_view(request):
    return settings.TEMPLATE.TemplateResponse(
        '/auth/login.html',
        {'request': request}
    )


routes = (
    Route('/login', login_view),
)

auth_views = Starlette(routes=routes)
