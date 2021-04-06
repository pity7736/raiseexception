import markdown

from raiseexception.blog.constants import PostState
from tests.factories import PostFactory, UserFactory


def test_lists_with_anonymous_user(db_connection, test_client, event_loop):
    author = event_loop.run_until_complete(UserFactory.create())
    draft_posts = event_loop.run_until_complete(
        PostFactory.create_batch(4, author=author)
    )
    posts = event_loop.run_until_complete(
        PostFactory.create_batch(5, author=author, state=PostState.PUBLISHED)
    )
    response = test_client.get('/blog')

    assert response.status_code == 200
    assert '<script async defer data-domain="raiseexception.dev"' \
        in response.text
    for post in posts:
        assert f'<h2>{post.title}</h2>' in response.text

    for post in draft_posts:
        assert f'<h2>{post.title}</h2>' not in response.text


def test_lists_with_authenticated_user(
        db_connection, test_client, event_loop, cookies_fixture):
    author = event_loop.run_until_complete(UserFactory.create())
    draft_posts = event_loop.run_until_complete(
        PostFactory.create_batch(4, author=author)
    )
    posts = event_loop.run_until_complete(
        PostFactory.create_batch(5, author=author, state=PostState.PUBLISHED)
    )
    response = test_client.get('/blog', cookies=cookies_fixture)

    assert response.status_code == 200
    assert '<script async defer data-domain="raiseexception.dev"' \
        not in response.text
    for post in posts:
        assert f'<h2>{post.title}</h2>' in response.text

    for post in draft_posts:
        assert f'<h2>{post.title}</h2>' in response.text


def test_published_post_detail(db_connection, test_client, event_loop):
    post = event_loop.run_until_complete(
        PostFactory.create(state=PostState.PUBLISHED)
    )
    response = test_client.get(f'/blog/{post.title_slug}')

    assert response.status_code == 200
    assert f'<h1>{post.title}</h1>' in response.text
    assert f'{markdown.markdown(post.body)}' in response.text
    assert f'<time datetime="{post.created_at.isoformat()}">{post.created_at}'\
           f'</time>' in response.text
    assert '<script async defer data-domain="raiseexception.dev"' \
        in response.text


def test_draft_post_detail_with_anonymous_user(db_connection, test_client,
                                               event_loop):
    post = event_loop.run_until_complete(PostFactory.create())
    response = test_client.get(f'/blog/{post.title_slug}')
    assert response.status_code == 404


def test_draft_post_detail_with_authenticated_user(
        db_connection, test_client, event_loop, cookies_fixture):
    post = event_loop.run_until_complete(PostFactory.create())
    response = test_client.get(
        f'/blog/{post.title_slug}',
        cookies=cookies_fixture
    )

    assert response.status_code == 200
    assert f'<h1>{post.title}</h1>' in response.text
    assert f'{markdown.markdown(post.body)}' in response.text
    assert f'<time datetime="{post.created_at.isoformat()}">{post.created_at}'\
           f'</time>' in response.text
    assert '<script async defer data-domain="raiseexception.dev"' \
        not in response.text


def test_post_detail_with_non_existing_post(db_connection, test_client):
    response = test_client.get('/blog/non-existing-post-title')
    assert response.status_code == 404


def test_post_detail_with_non_existing_post_with_authenticated_user(
        db_connection, test_client, cookies_fixture):
    response = test_client.get(
        '/blog/non-existing-post-title', cookies=cookies_fixture
    )
    assert response.status_code == 404
