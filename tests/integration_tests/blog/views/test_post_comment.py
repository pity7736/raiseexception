import asyncio

from raiseexception.blog.constants import PostState
from raiseexception.blog.models import PostComment
from raiseexception.mailing.client import MailClient
from tests.factories import PostFactory


def test_success(db_connection, test_client, event_loop, mocker):
    post = event_loop.run_until_complete(
        PostFactory.create(state=PostState.PUBLISHED)
    )
    mail_client_spy = mocker.spy(MailClient, 'send')
    response = test_client.post(
        f'/blog/{post.title_slug}',
        data={
            'name': 'Julián',
            'body': 'test comment',
            'email': 'anonymous@protonmail.com',
        }
    )
    comment = event_loop.run_until_complete(PostComment.get(post_id=post.id))

    assert response.status_code == 201
    assert comment.name == 'Julián'
    assert comment.post_id == post.id
    assert comment.email == 'anonymous@protonmail.com'
    assert "<p>The comment has been created in pending state. It will be " \
           "displayed when it's approved. I'll let you know by email if the " \
           "email was sent.</p>".replace("'", '&#39;') in response.text

    event_loop.run_until_complete(asyncio.sleep(1))
    assert mail_client_spy.spy_return is True
    mail_client_spy.assert_called_once()


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


def test_without_body(db_connection, test_client, event_loop):
    post = event_loop.run_until_complete(
        PostFactory.create(state=PostState.PUBLISHED)
    )
    response = test_client.post(
        f'/blog/{post.title_slug}',
        data={}
    )
    comment = event_loop.run_until_complete(
        PostComment.get_or_none(post_id=post.id)
    )

    assert response.status_code == 400
    assert comment is None


def test_with_wrong_email(db_connection, test_client, event_loop):
    post = event_loop.run_until_complete(
        PostFactory.create(state=PostState.PUBLISHED)
    )
    response = test_client.post(
        f'/blog/{post.title_slug}',
        data={
            'body': 'test comment',
            'post_id': post.id,
            'email': 'wrong @email'
        }
    )

    assert response.status_code == 400
    assert 'invalid email' in response.text
