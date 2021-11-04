import asyncio

import markdown
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.routing import Route

from raiseexception import settings
from raiseexception.blog.constants import PostState, PostCommentState
from raiseexception.blog.models import Post, PostComment
from raiseexception.mailing.client import MailClient
from raiseexception.mailing.models import To


def _filter_post_if_user_is_anonymous(user, queryset):
    if user.is_authenticated is False:
        # TODO: kinton - filter by using enum choice instead of enum value
        # example await Post.filter(state=PostState.PUBLISHED)
        queryset = queryset.filter(state=PostState.PUBLISHED.value)
    return queryset


async def posts_view(request: Request):
    queryset = _filter_post_if_user_is_anonymous(request.user, Post.filter())
    posts = await queryset
    return settings.TEMPLATE.TemplateResponse(
        name='/blog/posts.html',
        context={'request': request, 'posts': posts}
    )


async def post_detail_view(request: Request):
    queryset = Post.filter(title_slug=request.path_params['post_title'])
    queryset = _filter_post_if_user_is_anonymous(request.user, queryset)
    post = await queryset.get_or_none()
    if post is None:
        raise HTTPException(status_code=404)

    status_code = 200
    message = ''
    if request.method == 'POST':
        data = await request.form()
        body = data.get('body')
        status_code = 400
        if body:
            try:
                await PostComment.create(
                    post=post,
                    name=data.get('name') or None,
                    email=data.get('email'),
                    body=body
                )
            except ValueError:
                message = 'invalid email'
            else:
                status_code = 201
                message = (
                    "The comment has been created in pending state. It will "
                    "be displayed when it's approved. I'll let you know by "
                    "email if the email was sent."
                )
                mail_client = MailClient()
                asyncio.create_task(mail_client.send(
                    to=To(email=settings.ADMIN_EMAIL, name='Julián'),
                    subject='Comment created',
                    message=(
                        'You have a new comment to review. Check it <a href="'
                        f'{settings.SITE}/admin/blog/comments">here</a>'
                    )
                ))

    post_body = markdown.markdown(
        text=post.body,
        output_format='html5',
        extensions=[
            'codehilite',
            'fenced_code',
            'tables',
            'footnotes',
            'attr_list'
        ]
    )
    comments = await PostComment.filter(
        post_id=post.id,
        state=PostCommentState.APPROVED.value
    )
    return settings.TEMPLATE.TemplateResponse(
        name='/blog/post.html',
        status_code=status_code,
        context={
            'request': request,
            'post': post,
            'post_body': post_body,
            'comments': comments,
            'message': message
        }
    )


routes = (
    Route('/', posts_view),
    Route('/{post_title:str}', post_detail_view, methods=['GET', 'POST'])
)

blog_views = Starlette(routes=routes)
