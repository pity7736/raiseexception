import markdown
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.routing import Route

from raiseexception import settings
from raiseexception.blog.constants import PostState
from raiseexception.blog.models import Post


async def index(request: Request):
    # TODO: kinton - filter by using enum choice instead of enum value
    # example await Post.filter(state=PostState.PUBLISHED)
    queryset = Post.filter()
    if request.user.is_authenticated is False:
        queryset = queryset.filter(state=PostState.PUBLISHED.value)
    posts = await queryset
    return settings.TEMPLATE.TemplateResponse(
        name='/blog/posts.html',
        context={'request': request, 'posts': posts}
    )


async def post_detail(request: Request):
    queryset = Post.filter(title_slug=request.path_params['post_title'])
    if request.user.is_authenticated is False:
        queryset = queryset.filter(state=PostState.PUBLISHED.value)

    post = await queryset.get_or_none()
    if post is None:
        raise HTTPException(status_code=404)

    post_body = markdown.markdown(
        text=post.body,
        output_format='html5',
        extensions=['codehilite']
    )
    return settings.TEMPLATE.TemplateResponse(
        name='/blog/post.html',
        context={
            'request': request,
            'post': post,
            'post_body': post_body
        }
    )


routes = (
    Route('/', index),
    Route('/{post_title:str}', post_detail)
)

blog_views = Starlette(routes=routes)
