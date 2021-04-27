from raiseexception.subscription.models import Subscription


def test_success(db_connection, test_client, event_loop):
    token = 'token value'
    email = 'test@email.com'
    event_loop.run_until_complete(
        Subscription.create(email=email, token=token)
    )
    response = test_client.get(
        f'/subscription/verify?token={token}'
    )
    subscription = event_loop.run_until_complete(
        Subscription.get(email=email)
    )

    assert response.status_code == 200
    assert subscription.verified is True
    assert subscription.token is None
    assert 'email verified successfully' in response.text


def test_token_does_not_exists(db_connection, test_client, event_loop):
    token = 'token value'
    email = 'test@email.com'
    event_loop.run_until_complete(
        Subscription.create(email=email, token=token)
    )
    response = test_client.get(
        '/subscription/verify?token=wrong-token}'
    )
    subscription = event_loop.run_until_complete(
        Subscription.get(email=email)
    )

    assert response.status_code == 400
    assert subscription.verified is False
    assert subscription.token == token
    assert 'invalid token' in response.text


def test_with_more_than_one_subscription_with_token_none(
        db_connection, test_client, event_loop):
    event_loop.run_until_complete(
        Subscription.create(email='other@email.com', token='any token')
    )
    token = 'token value'
    email = 'test@email.com'
    event_loop.run_until_complete(
        Subscription.create(email=email, token=token)
    )
    response = test_client.get(
        f'/subscription/verify?token={token}'
    )
    subscription = event_loop.run_until_complete(
        Subscription.get(email=email)
    )

    assert response.status_code == 200
    assert subscription.verified is True
    assert subscription.token is None
    assert 'email verified successfully' in response.text
