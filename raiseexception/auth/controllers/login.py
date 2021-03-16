from raiseexception.auth.models import Token
from raiseexception.utils.crypto import make_password, get_random_string


async def login(user, password):
    unknown, salt, hashed_password = user.password.split('$')
    if f'{salt}${hashed_password}' == make_password(value=password, salt=salt):
        return await Token.create(
            value=get_random_string(length=64),
            user=user
        )
    return None
