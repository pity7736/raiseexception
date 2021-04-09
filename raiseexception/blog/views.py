import markdown
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse, PlainTextResponse
from starlette.routing import Route

from raiseexception import settings
from raiseexception.blog.constants import PostState
from raiseexception.blog.models import Post, PostComment


def _filter_post_if_user_is_anonymous(user, queryset):
    if user.is_authenticated is False:
        # TODO: kinton - filter by using enum choice instead of enum value
        # example await Post.filter(state=PostState.PUBLISHED)
        queryset = queryset.filter(state=PostState.PUBLISHED.value)
    return queryset


async def index(request: Request):
    queryset = _filter_post_if_user_is_anonymous(request.user, Post.filter())
    posts = await queryset
    return settings.TEMPLATE.TemplateResponse(
        name='/blog/posts.html',
        context={'request': request, 'posts': posts}
    )


async def post_detail(request: Request):
    queryset = Post.filter(title_slug=request.path_params['post_title'])
    queryset = _filter_post_if_user_is_anonymous(request.user, queryset)
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


async def post_comment(request):
    data = await request.form()
    post_id = data.get('post_id')
    body = data.get('body')
    if post_id and body:
        # TODO: cast to int - kinton
        post = await Post.get_or_none(id=int(post_id))
        if post is None:
            raise HTTPException(status_code=404)
        await PostComment.create(
            post=post,
            name=data.get('name'),
            email=data.get('email'),
            body=data['body']
        )
        return RedirectResponse(
            url=f'/blog/{post.title_slug}',
            status_code=302
        )
    return PlainTextResponse(status_code=400)


routes = (
    Route('/', index),
    Route('/comment', post_comment, methods=['POST']),
    Route('/{post_title:str}', post_detail)
)

blog_views = Starlette(routes=routes)
