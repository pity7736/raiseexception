from starlette.applications import Starlette
from starlette.responses import RedirectResponse
from starlette.routing import Route

from raiseexception import settings
from raiseexception.auth.controllers import login
from raiseexception.auth.decorators import redirect_if_is_authenticated


@redirect_if_is_authenticated
async def login_view(request):
    status_code = 200
    if request.method == 'POST':
        status_code = 401
        data = await request.form()
        username = data.get('username')
        password = data.get('password')
        if username and password:
            token = await login(username=username, password=password)
            if token:
                response = RedirectResponse(url='/', status_code=302)
                response.set_cookie(
                    key=settings.SESSION_COOKIE_NAME,
                    value=token.value,
                    domain='testserver.local',
                    secure=True,
                    httponly=True,
                    samesite='strict'
                )
                return response
    return settings.TEMPLATE.TemplateResponse(
        '/auth/login.html',
        {'request': request},
        status_code=status_code
    )


routes = (
    Route('/login', login_view, methods=['GET', 'POST'], name='login'),
)

auth_views = Starlette(routes=routes)
