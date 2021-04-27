from pytest import mark, raises

from raiseexception.mailing.models import Subscription


@mark.asyncio
async def test_create_with_name(db_connection):
    subscription = await Subscription.create(
        name='Julián',
        email='test@email.com'
    )

    assert subscription.name == 'Julián'
    assert subscription.email == 'test@email.com'
    assert subscription.verified is False
    assert subscription.created_at
    assert subscription.modified_at


@mark.asyncio
async def test_create_without_name(db_connection):
    subscription = await Subscription.create(
        email='test@email.com'
    )

    assert subscription.name == 'anonymous'
    assert subscription.email == 'test@email.com'
    assert subscription.verified is False
    assert subscription.created_at
    assert subscription.modified_at


invalid_email_params = (
    'wrong email',
    'wrong@email',

)


@mark.parametrize('email', invalid_email_params)
@mark.asyncio
async def test_create_with_wrong_email(email, db_connection):
    with raises(ValueError):
        await Subscription.create(email=email)
