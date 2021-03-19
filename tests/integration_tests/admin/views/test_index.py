from tests.factories import UserFactory


def test_anonymous(db_connection, test_client):
    response = test_client.get('/admin')
    last_page = response.history[-1]
    assert response.status_code == 200
    assert last_page.headers['location'] == '/auth/login?next=/admin'


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
