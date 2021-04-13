from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse, RedirectResponse
from starlette.routing import Route

from raiseexception import settings
from raiseexception.auth.decorators import login_required
from raiseexception.blog.constants import PostCommentState
from raiseexception.blog.controllers import CreatePost
from raiseexception.blog.models import Category, PostComment


@login_required
def index(request: Request):
    return PlainTextResponse(
        f'Hi, {request.user.username}',
        status_code=200
    )


@login_required
async def blog(request):
    status_code = 200
    message = ''
    if request.method == 'POST':
        data = await request.form()
        create_post = CreatePost(
            title=data.get('title'),
            body=data.get('body'),
            category_id=data.get('category_id'),
            author=request.user
        )
        try:
            await create_post.create()
        except ValueError as e:
            status_code = 400
            message = str(e)
        else:
            status_code = 201
            message = 'post created successfully'

    categories = await Category.all()
    return settings.TEMPLATE.TemplateResponse(
        name='/admin/blog.html',
        status_code=status_code,
        context={
            'request': request,
            'categories': categories,
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
        for comment_id in approved_comment_ids:
            comment = await PostComment.get(id=int(comment_id))
            comment.state = PostCommentState.APPROVED
            await comment.save(update_fields=('state', 'modified'))
        return RedirectResponse(url='/admin/blog/comments', status_code=302)

    return settings.TEMPLATE.TemplateResponse(
        name='/admin/comments.html',
        context={'request': request, 'comments': comments}
    )


routes = (
    Route('/', index),
    Route('/blog', blog, methods=['GET', 'POST']),
    Route('/blog/comments', comments_view, methods=['GET', 'POST'])
)

admin_views = Starlette(routes=routes)
