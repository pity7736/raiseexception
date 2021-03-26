from tests.factories import PostFactory, UserFactory


def test_lists(db_connection, test_client, event_loop):
    author = event_loop.run_until_complete(UserFactory.create())
    posts = event_loop.run_until_complete(
        PostFactory.create_batch(5, author=author)
    )
    response = test_client.get('/blog')

    assert response.status_code == 200
    for post in posts:
        assert f'<h2>{post.title}</h2>' in response.text


def test_post_detail(db_connection, test_client, event_loop):
    post = event_loop.run_until_complete(PostFactory.create())
    response = test_client.get(f'/blog/{post.title_slug}')

    assert response.status_code == 200
    assert f'<h1>{post.title}</h1>' in response.text
    assert f'{post.body}' in response.text


def test_post_detail_with_non_existing_post(db_connection, test_client):
    response = test_client.get('/blog/non-existing-post-title')

    assert response.status_code == 404
