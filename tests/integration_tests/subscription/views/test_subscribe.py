
def test_subscribe_get(db_connection, test_client):
    response = test_client.get('/subscription')
    assert '<form id="subscribe" method="post"' in response.text
