from raiseexception import settings
from raiseexception.auth.models import Token
from tests.factories import UserFactory


def test_get(test_client, cookies_fixture):
    response = test_client.get(
        '/auth/logout',
        allow_redirects=False,
        cookies=cookies_fixture
    )
    assert response.status_code == 301
    assert response.headers['location'] == '/'


def test_success(db_connection, event_loop, test_client, cookies_fixture):
    response = test_client.post(
        '/auth/logout',
        cookies=cookies_fixture
    )

    cookie_header = response.headers['set-cookie']
    tokens = event_loop.run_until_complete(Token.all())

    assert response.status_code == 302
    assert f'{settings.SESSION_COOKIE_NAME}=""' in cookie_header
    assert len(tokens) == 0


def test_without_session_cookie(db_connection, test_client):
    response = test_client.post(
        '/auth/logout'
    )
    assert response.status_code == 302
    assert response.headers['location'] == '/auth/login?next=/auth/logout'


def test_with_two_tokens_created(db_connection, test_client, event_loop,
                                 cookies_fixture):
    test_client.post(
        '/auth/login',
        data={
            'username': UserFactory.username,
            'password': UserFactory.password
        }
    )
    response = test_client.post(
        '/auth/logout',
        cookies=cookies_fixture
    )

    cookie_header = response.headers['set-cookie']
    tokens = event_loop.run_until_complete(Token.all())

    assert response.status_code == 302
    assert f'{settings.SESSION_COOKIE_NAME}=""' in cookie_header
    assert len(tokens) == 1
