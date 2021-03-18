from starlette.applications import Starlette
from starlette.responses import RedirectResponse
from starlette.routing import Route

from raiseexception import settings
from raiseexception.auth.controllers import login


async def login_view(request):
    status_code = 200
    if request.method == 'POST':
        status_code = 401
        data = await request.form()
        username = data.get('username')
        password = data.get('password')
        token = await login(username=username, password=password)
        response = RedirectResponse(url='/', status_code=302)
        if token:
            response.set_cookie(
                key='__Host-raiseexception-session',
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
    Route('/login', login_view, methods=['GET', 'POST']),
)

auth_views = Starlette(routes=routes)
