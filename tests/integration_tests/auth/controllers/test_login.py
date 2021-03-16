from pytest import mark

from raiseexception import settings
from raiseexception.auth.controllers import login
from raiseexception.auth.models import Token
from tests.factories import UserFactory


@mark.asyncio
async def test_success(db_connection):
    user = await UserFactory.create()

    token = await login(username=user.username, password=UserFactory.password)

    assert isinstance(token, Token)
    assert token.value
    assert len(token.value) == settings.SESSION_TOKEN_LENGTH
    assert token.user.id == user.id


@mark.asyncio
async def test_fail(db_connection):
    user = await UserFactory.create()
    token = await login(
        username=user.username,
        password=UserFactory.password + 'other word'
    )
    assert token is None


@mark.asyncio
async def test_user_does_not_exists(db_connection):
    await UserFactory.create()
    token = await login(
        username='wrong username',
        password=UserFactory.password + 'other word'
    )
    assert token is None
