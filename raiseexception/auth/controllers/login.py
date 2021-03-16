from raiseexception import settings
from raiseexception.accounts.models import User
from raiseexception.auth.models import Token
from raiseexception.utils.crypto import make_password, get_random_string


async def login(username, password):
    user = await User.get_or_none(username=username)
    if user:
        salt, hashed_password = user.password.split('$')
        if user.password == make_password(value=password, salt=salt):
            return await Token.create(
                value=get_random_string(length=settings.SESSION_TOKEN_LENGTH),
                user=user
            )
    return None
