from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse, RedirectResponse
from starlette.routing import Route

from raiseexception import settings
from raiseexception.auth.models import Token


async def index(request: Request):
    session_token = request.cookies.get(settings.SESSION_COOKIE_NAME)
    if session_token:
        token = await Token.get_or_none(value=session_token)
        if token:
            await token.user.fetch()
            return PlainTextResponse(
                f'Hi, {token.user.username}',
                status_code=200
            )
    return RedirectResponse(url='/auth/login?next=/admin', status_code=302)

routes = (
    Route('/', index),
)

admin_views = Starlette(routes=routes)
