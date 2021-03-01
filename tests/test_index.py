from starlette.testclient import TestClient

from raiseexception.app import app


def test_homepage():
    client = TestClient(app=app)
    response = client.get("/")

    assert response.status_code == 200
    assert response.template.name == 'index.html'
    assert "<title>Julián Cortés' personal website</title>" in response.text
