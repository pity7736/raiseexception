from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Route

from raiseexception import settings
from raiseexception.blog.models import Post


async def index(request: Request):
    posts = await Post.all()
    return settings.TEMPLATE.TemplateResponse(
        name='/blog/posts.html',
        context={'request': request, 'posts': posts}
    )


routes = (
    Route('/', index),
)

blog_views = Starlette(routes=routes)
