import asyncio
import datetime

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse, RedirectResponse
from starlette.routing import Route

from raiseexception import settings
from raiseexception.auth.decorators import login_required
from raiseexception.blog.constants import PostCommentState, PostState
from raiseexception.blog.controllers import CreatePost
from raiseexception.blog.models import Category, PostComment, Post
from raiseexception.mailing.client import MailClient
from raiseexception.mailing.models import To
from raiseexception.subscription.models import Subscription


@login_required
def index(request: Request):
    return PlainTextResponse(
        f'Hi, {request.user.username}',
        status_code=200
    )


@login_required
async def posts_view(request):
    status_code = 200
    message = ''
    if request.method == 'POST':
        data = await request.form()
        create_post = CreatePost(
            title=data.get('title'),
            body=data.get('body'),
            category_id=data.get('category_id'),
            author=request.user,
            description=data.get('description')
        )
        try:
            await create_post.create()
        except ValueError as e:
            status_code = 400
            message = str(e)
        else:
            status_code = 201
            message = 'post created successfully'

    # improve testing to be able to run queries concurrently
    categories = await Category.all()
    posts = await Post.all()
    return settings.TEMPLATE.TemplateResponse(
        name='/admin/blog.html',
        status_code=status_code,
        context={
            'request': request,
            'categories': categories,
            'posts': posts,
            'message': message
        }
    )


@login_required
async def comments_view(request: Request):
    pending_comments = await PostComment.filter(
        state=PostCommentState.PENDING.value
    )
    comments = []
    # TODO: kinton - refactor this using prefetch from DB
    for pending_comment in pending_comments:
        await pending_comment.post.fetch()
        comments.append(pending_comment)
    if request.method == 'POST':
        data = await request.form()
        approved_comment_ids = data.getlist('approve')
        # TODO: kinton - refactor this implementing update method and in lookup
        mail_client = MailClient()
        mail_tasks = []
        for comment_id in approved_comment_ids:
            comment = await PostComment.get(id=int(comment_id))
            comment.state = PostCommentState.APPROVED
            await comment.save(update_fields=('state', 'modified'))
            if comment.email:
                await comment.post.fetch()
                post = comment.post
                mail_tasks.append(mail_client.send(
                    to=To(email=comment.email, name=comment.name),
                    subject='Comment approved',
                    message=f'Hi {comment.name}, you comment was approved. '
                            f'Check it <a href="{settings.SITE}/blog'
                            f'/{post.title_slug}">here</a>'
                ))
        await asyncio.gather(*mail_tasks)
        return RedirectResponse(url='/admin/blog/comments', status_code=302)

    return settings.TEMPLATE.TemplateResponse(
        name='/admin/comments.html',
        context={'request': request, 'comments': comments}
    )


@login_required
async def post_detail_view(request: Request):
    post = await Post.get(title_slug=request.path_params['post_title'])
    categories = await Category.all()
    message = ''
    status_code = 200
    if request.method == 'POST':
        data = await request.form()
        message = 'post updated successfully'
        for key, value in data.items():
            # TODO: validate that the body is a valid markdown
            if hasattr(post, key):
                setattr(post, key, value)
            else:
                message = f'"{key}" is an invalid field'
                status_code = 400
                break
        else:
            await post.save()
    return settings.TEMPLATE.TemplateResponse(
        name='/admin/post.html',
        status_code=status_code,
        context={
            'request': request,
            'post': post,
            'categories': categories,
            'message': message
        }
    )


@login_required
async def publish_post_view(request: Request):
    data = await request.form()
    post = await Post.get(id=int(data['post_id']))
    post.state = PostState.PUBLISHED
    post.published_at = datetime.datetime.now()
    await post.save()
    subscriptions = await Subscription.filter(verified=True)
    email_client = MailClient()
    emails_to_send = []
    for subscription in subscriptions:
        emails_to_send.append(email_client.send(
            to=To(email=subscription.email, name=subscription.name),
            subject='A new post was published!',
            message=f'Hi {subscription.name}, a new post was published. Read '
                    f'it <a href="{settings.SITE}/blog/{post.title_slug}?'
                    f'utm_campaign=Newsletter&utm_medium=Email'
                    f'&utm_source=Email">here</a>'
        ))
    await asyncio.gather(*emails_to_send)
    return RedirectResponse(
        url=f'/admin/blog/{post.title_slug}',
        status_code=302
    )


routes = (
    Route('/', index),
    Route('/blog', posts_view, methods=['GET', 'POST']),
    Route('/blog/comments', comments_view, methods=['GET', 'POST']),
    Route('/blog/publish', publish_post_view, methods=['POST']),
    Route('/blog/{post_title:str}', post_detail_view, methods=['GET', 'POST'])
)

admin_views = Starlette(routes=routes)
