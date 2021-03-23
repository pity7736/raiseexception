import asyncio

from starlette.requests import Request
from starlette.responses import RedirectResponse


def login_required(function):
    async def wrapper(request: Request):
        if request.user.is_authenticated:
            if asyncio.iscoroutinefunction(function):
                return await function(request)
            else:
                return function(request)
        return RedirectResponse(
            url=f'/auth/login?next={request.url.path}',
            status_code=302
        )
    return wrapper


def redirect_if_is_authenticated(function):
    async def wrapper(request: Request):
        if request.user.is_authenticated:
            return RedirectResponse(url='/', status_code=302)
        return await function(request)
    return wrapper
