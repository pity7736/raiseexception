from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route

from raiseexception import settings
from raiseexception.auth.decorators import login_required
from raiseexception.blog.models import Category


@login_required
def index(request: Request):
    return PlainTextResponse(
        f'Hi, {request.user.username}',
        status_code=200
    )


@login_required
async def blog(request):
    categories = await Category.all()
    return settings.TEMPLATE.TemplateResponse(
        '/admin/blog.html',
        {'request': request, 'categories': categories}
    )


routes = (
    Route('/', index),
    Route('/blog', blog)
)

admin_views = Starlette(routes=routes)
