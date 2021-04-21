from unittest.mock import AsyncMock

from raiseexception.blog.constants import PostState, PostCommentState
from raiseexception.blog.models import PostComment
from raiseexception.mailing.client import MailClient
from tests.factories import PostFactory, PostCommentFactory


def test_list_comments(db_connection, test_client, event_loop,
                       cookies_fixture):
    post = event_loop.run_until_complete(
        PostFactory.create(state=PostState.PUBLISHED)
    )
    comments = event_loop.run_until_complete(
        PostCommentFactory.create_batch(5, post=post)
    )
    response = test_client.get(
        '/admin/blog/comments',
        cookies=cookies_fixture
    )

    assert response.status_code == 200
    assert 'Pending comments:' in response.text
    for comment in comments:
        assert comment.name in response.text
        assert comment.post.title in response.text
        assert f'<input name="approve" type="checkbox" value="{post.id}">' \
            in response.text


def test_approve_comments(db_connection, test_client, event_loop,
                          cookies_fixture, mocker):
    post = event_loop.run_until_complete(
        PostFactory.create(state=PostState.PUBLISHED)
    )
    comments = event_loop.run_until_complete(
        PostCommentFactory.create_batch(5, post=post)
    )
    mail_client_spy = mocker.patch.object(
        MailClient,
        'send',
        new_callable=AsyncMock
    )
    response = test_client.post(
        '/admin/blog/comments',
        data={'approve': [comment.id for comment in comments]},
        cookies=cookies_fixture
    )
    comments = event_loop.run_until_complete(PostComment.all())

    assert response.status_code == 302
    for comment in comments:
        assert comment.state == PostCommentState.APPROVED
    assert mail_client_spy.await_count == 5


def test_list_comments_with_no_pending_comments(db_connection, test_client,
                                                event_loop, cookies_fixture):
    post = event_loop.run_until_complete(
        PostFactory.create(state=PostState.PUBLISHED)
    )
    event_loop.run_until_complete(
        PostCommentFactory.create_batch(
            5,
            post=post,
            state=PostCommentState.APPROVED
        )
    )
    response = test_client.get(
        '/admin/blog/comments',
        cookies=cookies_fixture
    )

    assert response.status_code == 200
    assert 'Pending comments:' not in response.text
    assert 'There are no pending comments.' in response.text
