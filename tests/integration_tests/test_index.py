
def test_homepage(test_client):
    response = test_client.get("/")

    assert response.status_code == 200
    assert response.template.name == 'index.html'
    assert "<title>Julián Cortés' personal website</title>" in response.text
