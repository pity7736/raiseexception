from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Route

from raiseexception import settings


async def subscribe_view(request: Request):
    return settings.TEMPLATE.TemplateResponse(
        name='/subscription/subscribe.html',
        context={'request': request}
    )


routes = (
    Route('/', subscribe_view),
)

subscription_views = Starlette(routes=routes)
