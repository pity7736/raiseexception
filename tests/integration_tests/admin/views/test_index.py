from tests.factories import UserFactory


def test_anonymous(db_connection, test_client):
    response = test_client.get('/admin')
    location = response.history[-1].headers['location']
    assert response.status_code == 200
    assert location == '/auth/login?next=/admin/'


def test_authenticated(db_connection, event_loop, test_client):
    user = event_loop.run_until_complete(UserFactory.create())
    login_response = test_client.post(
        '/auth/login',
        data={'username': user.username, 'password': UserFactory.password}
    )
    response = test_client.get(
        '/admin',
        cookies=login_response.cookies.get_dict()
    )

    assert response.status_code == 200
    assert f'Hi, {user.username}' in response.text


def test_redirect_to_next_after_login(db_connection, event_loop, test_client):
    user = event_loop.run_until_complete(UserFactory.create())
    first_response = test_client.get('/admin/blog')
    location = first_response.history[-1].headers['location']
    response = test_client.post(
        location,
        data={'username': user.username, 'password': UserFactory.password}
    )

    assert response.headers['location'] == '/admin/blog'
