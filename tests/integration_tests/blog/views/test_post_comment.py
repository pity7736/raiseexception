from raiseexception.blog.constants import PostState
from raiseexception.blog.models import PostComment
from tests.factories import PostFactory


def test_success(db_connection, test_client, event_loop):
    post = event_loop.run_until_complete(
        PostFactory.create(state=PostState.PUBLISHED)
    )
    response = test_client.post(
        f'/blog/{post.title_slug}',
        data={
            'name': 'Julián',
            'body': 'test comment',
            'email': 'anonymous@protonmail.com',
            'post_id': post.id
        }
    )
    comment = event_loop.run_until_complete(PostComment.get(post_id=post.id))

    assert response.status_code == 201
    assert comment.name == 'Julián'
    assert comment.post_id == post.id
    assert comment.email == 'anonymous@protonmail.com'
    assert "<p>The comment has been created in pending state. It will be " \
           "displayed when it's approved. I'll let you know by email if the " \
           "email was sent.</p>"


def test_without_email(db_connection, test_client, event_loop):
    post = event_loop.run_until_complete(
        PostFactory.create(state=PostState.PUBLISHED)
    )
    response = test_client.post(
        f'/blog/{post.title_slug}',
        data={
            'name': 'Julián',
            'body': 'test comment',
            'post_id': post.id
        }
    )
    comment = event_loop.run_until_complete(PostComment.get(post_id=post.id))

    assert response.status_code == 201
    assert comment.name == 'Julián'
    assert comment.post_id == post.id
    assert comment.email is None


def test_without_name(db_connection, test_client, event_loop):
    post = event_loop.run_until_complete(
        PostFactory.create(state=PostState.PUBLISHED)
    )
    response = test_client.post(
        f'/blog/{post.title_slug}',
        data={
            'body': 'test comment',
            'post_id': post.id,
            'email': 'anonymous@protonmail.com'
        }
    )
    comment = event_loop.run_until_complete(PostComment.get(post_id=post.id))

    assert response.status_code == 201
    assert comment.name == 'anonymous'
    assert comment.post_id == post.id
    assert comment.email == 'anonymous@protonmail.com'


def test_without_name_or_email(db_connection, test_client, event_loop):
    post = event_loop.run_until_complete(
        PostFactory.create(state=PostState.PUBLISHED)
    )
    response = test_client.post(
        f'/blog/{post.title_slug}',
        data={
            'body': 'test comment',
            'post_id': post.id,
        }
    )
    comment = event_loop.run_until_complete(PostComment.get(post_id=post.id))

    assert response.status_code == 201
    assert comment.name == 'anonymous'
    assert comment.post_id == post.id
    assert comment.email is None


def test_without_post_id(db_connection, test_client, event_loop):
    post = event_loop.run_until_complete(
        PostFactory.create(state=PostState.PUBLISHED)
    )
    response = test_client.post(
        f'/blog/{post.title_slug}',
        data={
            'body': 'test comment',
        }
    )
    comment = event_loop.run_until_complete(
        PostComment.get_or_none(post_id=post.id)
    )

    assert response.status_code == 400
    assert comment is None


def test_without_body(db_connection, test_client, event_loop):
    post = event_loop.run_until_complete(
        PostFactory.create(state=PostState.PUBLISHED)
    )
    response = test_client.post(
        f'/blog/{post.title_slug}',
        data={
            'post_id': post.id
        }
    )
    comment = event_loop.run_until_complete(
        PostComment.get_or_none(post_id=post.id)
    )

    assert response.status_code == 400
    assert comment is None


def test_with_wrong_post_id(db_connection, test_client, event_loop):
    post = event_loop.run_until_complete(
        PostFactory.create(state=PostState.PUBLISHED)
    )
    response = test_client.post(
        f'/blog/{post.title_slug}',
        data={
            'post_id': 100000000,
            'body': 'test comment'
        }
    )
    comment = event_loop.run_until_complete(
        PostComment.get_or_none(post_id=post.id)
    )

    assert response.status_code == 404
    assert comment is None
