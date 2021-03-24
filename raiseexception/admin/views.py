from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route

from raiseexception import settings
from raiseexception.auth.decorators import login_required
from raiseexception.blog.controllers import CreatePost
from raiseexception.blog.models import Category


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


routes = (
    Route('/', index),
    Route('/blog', blog, methods=['GET', 'POST'])
)

admin_views = Starlette(routes=routes)
