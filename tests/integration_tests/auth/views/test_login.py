from tests.factories import UserFactory


def test_get(test_client):
    response = test_client.get('/auth/login')

    assert response.status_code == 200
    assert '<form id="login" action="/auth/login" method="post">' \
           in response.text
    assert '<label for="username">Username:</label>' in response.text
    assert '<input id="username" name="username" type="text" required ' \
           'autofocus>' in response.text
    assert '<label for="password">Password:</label>' in response.text
    assert '<input id="password" name="password" type="password" ' \
           'required>' in response.text
    assert '<input type="submit" value="login">' in response.text
    assert '</form>' in response.text


def test_post_success(db_connection, event_loop, test_client):
    user = event_loop.run_until_complete(UserFactory.create())
    response = test_client.post(
        '/auth/login',
        data={'username': user.username, 'password': UserFactory.password}
    )
    session_cookie = response.cookies['__Host-raiseexception-session']

    assert response.status_code == 307
    assert session_cookie


def test_wrong_password(db_connection, event_loop, test_client):
    user = event_loop.run_until_complete(UserFactory.create())
    response = test_client.post(
        '/auth/login',
        data={'username': user.username, 'password': 'wrong password'}
    )
    session_cookie = response.cookies.get('__Host-raiseexception-session')

    assert response.status_code == 401
    assert session_cookie is None
