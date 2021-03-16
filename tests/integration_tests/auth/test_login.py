from pytest import mark

from raiseexception.accounts.models import User
from raiseexception.auth.controllers import login
from raiseexception.auth.models import Token


@mark.asyncio
async def test_success(db_connection):
    password = 'test password'
    user = await User.create(
        username='__pity__',
        email='test@email.com',
        password=password
    )

    token = await login(user=user, password=password)

    assert isinstance(token, Token)
    assert token.value
    assert token.user.id == user.id


@mark.asyncio
async def test_fail(db_connection):
    password = 'test password'
    user = await User.create(
        username='__pity__',
        email='test@email.com',
        password=password
    )

    token = await login(user=user, password=password + 'other word')

    assert token is None
