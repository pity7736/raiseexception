from starlette.applications import Starlette
from starlette.exceptions import HTTPException
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


async def post_detail(request: Request):
    post = await Post.get_or_none(title_slug=request.path_params['post_title'])
    if post is None:
        raise HTTPException(status_code=404)
    return settings.TEMPLATE.TemplateResponse(
        name='/blog/post.html',
        context={'request': request, 'post': post}
    )


routes = (
    Route('/', index),
    Route('/{post_title:str}', post_detail)
)

blog_views = Starlette(routes=routes)
