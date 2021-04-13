import markdown

from raiseexception.blog.constants import PostState, PostCommentState
from raiseexception.blog.models import PostComment
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
        assert f'<h2><a href="/blog/{post.title_slug}">{post.title}</a></h2>'\
            in response.text

    for post in draft_posts:
        assert f'<h2><a href="/blog/{post.title_slug}">{post.title}</a></h2>'\
            not in response.text


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
        assert f'<h2><a href="/blog/{post.title_slug}">{post.title}</a></h2>'\
            in response.text

    for post in draft_posts:
        assert f'<h2><a href="/blog/{post.title_slug}">{post.title}</a></h2>'\
            in response.text


def test_published_post_detail(db_connection, test_client, event_loop):
    post = event_loop.run_until_complete(
        PostFactory.create(state=PostState.PUBLISHED)
    )
    post_comment = event_loop.run_until_complete(PostComment.create(
        name='test name',
        email='raiseexception@pm.me',
        body='comment body',
        post=post,
        state=PostCommentState.APPROVED
    ))
    response = test_client.get(f'/blog/{post.title_slug}')

    assert response.status_code == 200
    assert f'<h1>{post.title}</h1>' in response.text
    assert f'{markdown.markdown(post.body)}' in response.text
    assert f'<time datetime="{post.created_at.isoformat()}">{post.created_at}'\
           f'</time>' in response.text
    assert '<script async defer data-domain="raiseexception.dev"' \
        in response.text
    assert '<form id="comment" method="post">' \
        in response.text
    assert '<label for="name">Name:</label>' in response.text
    assert '<input id="name" name="name" type="text" placeholder=' \
        '"name or alias">' in response.text
    assert '<label for="email">Email:</label>' in response.text
    assert '<input id="email" name="email" type="email" placeholder=' \
        '"email will not be published"' in response.text
    assert '<label for="body">Comment:</label>' in response.text
    assert '<textarea id="body" name="body" required></textarea>' \
        in response.text
    assert '<input type="submit" value="Comment">' in response.text
    assert 'Comments:' in response.text
    assert f'{post_comment.name}, {post_comment.created_at}' in response.text
    assert f'<p>{post_comment.body}</p>' in response.text


def test_published_post_detail_with_pending_comment(db_connection, test_client,
                                                    event_loop):
    post = event_loop.run_until_complete(
        PostFactory.create(state=PostState.PUBLISHED)
    )
    post_comment = event_loop.run_until_complete(PostComment.create(
        name='test name',
        email='raiseexception@pm.me',
        body='comment body',
        post=post
    ))
    response = test_client.get(f'/blog/{post.title_slug}')

    assert response.status_code == 200
    assert f'<h1>{post.title}</h1>' in response.text
    assert f'{markdown.markdown(post.body)}' in response.text
    assert f'<time datetime="{post.created_at.isoformat()}">{post.created_at}'\
           f'</time>' in response.text
    assert '<script async defer data-domain="raiseexception.dev"' \
        in response.text
    assert '<form id="comment" method="post">' \
        in response.text
    assert '<label for="name">Name:</label>' in response.text
    assert '<input id="name" name="name" type="text" placeholder=' \
        '"name or alias">' in response.text
    assert '<label for="email">Email:</label>' in response.text
    assert '<input id="email" name="email" type="email" placeholder=' \
        '"email will not be published"' in response.text
    assert '<label for="body">Comment:</label>' in response.text
    assert '<textarea id="body" name="body" required></textarea>' \
        in response.text
    assert '<input type="submit" value="Comment">' in response.text
    assert 'Comments:' not in response.text
    assert f'{post_comment.name}, {post_comment.created_at}' not in \
        response.text
    assert f'<p>{post_comment.body}</p>' not in response.text
    assert '<p>There are no comments.</p>'


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
