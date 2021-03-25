from tests.factories import PostFactory, UserFactory


def test_simple(db_connection, test_client, event_loop):
    author = event_loop.run_until_complete(UserFactory.create())
    posts = event_loop.run_until_complete(
        PostFactory.create_batch(5, author=author)
    )
    response = test_client.get('/blog')

    assert response.status_code == 200
    for post in posts:
        assert f'<h2>{post.title}</h2>' in response.text
