from raiseexception.mailing.client import MailClient
from raiseexception.subscription.models import Subscription


def test_subscribe_get(db_connection, test_client):
    response = test_client.get('/subscription')
    assert '<form id="subscribe" method="post"' in response.text


def test_subscribe(db_connection, test_client, event_loop, mocker):
    mail_client_spy = mocker.spy(MailClient, 'send')
    response = test_client.post(
        '/subscription/',
        data={
            'name': 'Julián',
            'email': 'test@email.com'
        }
    )
    subscription = event_loop.run_until_complete(
        Subscription.get()
    )

    assert response.status_code == 201
    assert subscription.name == 'Julián'
    assert subscription.email == 'test@email.com'
    assert subscription.token
    assert 'Subscription created. I sent you a email to verify it.' \
        in response.text
    mail_client_spy.assert_called_once()


def test_subscribe_without_name(db_connection, test_client, event_loop):
    response = test_client.post(
        '/subscription/',
        data={
            'email': 'test@email.com'
        }
    )
    subscription = event_loop.run_until_complete(
        Subscription.get()
    )

    assert response.status_code == 201
    assert subscription.name == 'anonymous'
    assert subscription.email == 'test@email.com'


def test_subscribe_without_email(db_connection, test_client, event_loop):
    response = test_client.post(
        '/subscription/',
        data={
            'name': 'Julián'
        }
    )
    subscription = event_loop.run_until_complete(
        Subscription.get_or_none()
    )

    assert response.status_code == 400
    assert subscription is None
    assert 'email is required' in response.text


def test_subscribe_with_existing_email(db_connection, test_client, event_loop):
    email = 'test@email.com'
    event_loop.run_until_complete(
        Subscription.create(email=email)
    )
    response = test_client.post(
        '/subscription/',
        data={
            'email': email
        }
    )
    subscription = event_loop.run_until_complete(
        Subscription.get(email=email)
    )

    assert response.status_code == 400
    assert subscription.email == email
    assert 'the email was already subscribed' in response.text


def test_with_wrong_email(test_client):
    response = test_client.post(
        '/subscription/',
        data={'email': 'wrong email'}
    )

    assert response.status_code == 400
    assert 'invalid email' in response.text
