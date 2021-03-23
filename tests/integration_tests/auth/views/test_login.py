from raiseexception import settings
from tests.factories import UserFactory


def test_get(test_client):
    response = test_client.get('/auth/login')

    assert response.status_code == 200
    assert '<form id="login" action="#" method="post">' \
           in response.text
    assert '<label for="username">Username:</label>' in response.text
    assert '<input id="username" name="username" type="text" required ' \
           'autofocus>' in response.text
    assert '<label for="password">Password:</label>' in response.text
    assert '<input id="password" name="password" type="password" ' \
           'required>' in response.text
    assert '<input type="submit" value="login">' in response.text
    assert '</form>' in response.text


def test_get_already_logged(db_connection, event_loop, test_client):
    user = event_loop.run_until_complete(UserFactory.create())
    login_response = test_client.post(
        '/auth/login',
        data={'username': user.username, 'password': UserFactory.password}
    )
    response = test_client.get(
        '/auth/login',
        cookies=login_response.cookies.get_dict(),
        allow_redirects=False
    )
    assert response.status_code == 302


def test_get_with_fake_cookie(db_connection, event_loop, test_client):
    user = event_loop.run_until_complete(UserFactory.create())
    test_client.post(
        '/auth/login',
        data={'username': user.username, 'password': UserFactory.password}
    )
    response = test_client.get(
        '/auth/login',
        cookies={settings.SESSION_COOKIE_NAME: 'token value'},
        allow_redirects=False
    )
    assert response.status_code == 200


def test_post_success(db_connection, event_loop, test_client):
    user = event_loop.run_until_complete(UserFactory.create())
    response = test_client.post(
        '/auth/login',
        data={'username': user.username, 'password': UserFactory.password}
    )
    session_cookie = response.cookies[settings.SESSION_COOKIE_NAME]

    assert response.status_code == 302
    assert session_cookie


def test_post_with_json(db_connection, event_loop, test_client):
    user = event_loop.run_until_complete(UserFactory.create())
    response = test_client.post(
        '/auth/login',
        json={'username': user.username, 'password': UserFactory.password}
    )
    session_cookie = response.cookies.get(settings.SESSION_COOKIE_NAME)

    assert response.status_code == 401
    assert session_cookie is None


def test_wrong_password(db_connection, event_loop, test_client):
    user = event_loop.run_until_complete(UserFactory.create())
    response = test_client.post(
        '/auth/login',
        data={'username': user.username, 'password': 'wrong password'}
    )
    session_cookie = response.cookies.get(settings.SESSION_COOKIE_NAME)

    assert response.status_code == 401
    assert session_cookie is None


def test_without_username_and_password(db_connection, event_loop, test_client):
    event_loop.run_until_complete(UserFactory.create())
    response = test_client.post(
        '/auth/login',
        data={'username': None, 'password': None}
    )
    session_cookie = response.cookies.get(settings.SESSION_COOKIE_NAME)

    assert response.status_code == 401
    assert session_cookie is None


def test_user_does_not_exists(db_connection, event_loop, test_client):
    event_loop.run_until_complete(UserFactory.create())
    response = test_client.post(
        '/auth/login',
        data={'username': 'wrong username', 'password': UserFactory.password}
    )
    session_cookie = response.cookies.get(settings.SESSION_COOKIE_NAME)

    assert response.status_code == 401
    assert session_cookie is None


def test_domain(db_connection, event_loop, test_client):
    current_domain = settings.APP_DOMAIN
    settings.APP_DOMAIN = 'raiseexception.dev'
    test_client.base_url = f'http://{settings.APP_DOMAIN}'
    user = event_loop.run_until_complete(UserFactory.create())
    response = test_client.post(
        '/auth/login',
        data={'username': user.username, 'password': UserFactory.password},
    )
    session_cookie = response.cookies.get(
        name=settings.SESSION_COOKIE_NAME,
        domain=f'.{settings.APP_DOMAIN}',
    )

    assert session_cookie
    settings.APP_DOMAIN = current_domain
