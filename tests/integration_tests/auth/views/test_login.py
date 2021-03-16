from starlette.testclient import TestClient

from raiseexception import app


def test_get():
    client = TestClient(app=app)
    response = client.get('/auth/login')

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
