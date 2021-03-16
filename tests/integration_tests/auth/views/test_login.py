from starlette.testclient import TestClient

from raiseexception import app


def test_get(db_connection):
    client = TestClient(app=app)
    response = client.get('/auth/login')

    assert response.status_code == 200
    assert '' in response.text
