
def test_homepage_with_anonymous_user(test_client):
    response = test_client.get("/")

    assert response.status_code == 200
    assert response.template.name == 'index.html'
    assert "<title>Raise Exception | Julián Cortés Personal Website</title>" \
        in response.text
    assert '<script async defer data-domain="raiseexception.dev"' \
        in response.text


def test_homepage_with_authenticated_user(db_connection, test_client,
                                          cookies_fixture):
    response = test_client.get("/", cookies=cookies_fixture)

    assert response.status_code == 200
    assert response.template.name == 'index.html'
    assert "<title>Raise Exception | Julián Cortés Personal Website</title>" \
        in response.text
    assert '<script async defer data-domain="raiseexception.dev"' \
        not in response.text
