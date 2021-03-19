from starlette.authentication import AuthenticationBackend, AuthCredentials, \
    AuthenticationError
from starlette.requests import HTTPConnection

from raiseexception import settings
from raiseexception.auth.models import Token


class CookieAuthBackend(AuthenticationBackend):

    async def authenticate(self, conn: HTTPConnection):
        session_token = conn.cookies.get(settings.SESSION_COOKIE_NAME)
        if not session_token:
            return

        token = await Token.get_or_none(value=session_token)
        if token:
            await token.user.fetch()
            return AuthCredentials(), token.user
        elif conn.url.path == '/auth/login':
            return
        raise AuthenticationError('invalid token')
