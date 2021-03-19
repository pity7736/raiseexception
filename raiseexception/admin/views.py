from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route

from raiseexception.auth.decorators import login_required


@login_required
def index(request: Request):
    return PlainTextResponse(
        f'Hi, {request.user.username}',
        status_code=200
    )


routes = (
    Route('/', index),
)

admin_views = Starlette(routes=routes)
