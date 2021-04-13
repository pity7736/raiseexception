from pytest import mark

from raiseexception.blog.constants import PostCommentState
from raiseexception.blog.models import PostComment
from tests.factories import PostFactory


@mark.asyncio
async def test_success(db_connection):
    post = await PostFactory.create()
    comment = await PostComment.create(
        post=post,
        name='Julián',
        email='anonymous@protonmail.com',
        body='I like this post'
    )
    comment = await PostComment.get(id=comment.id)
    await comment.post.fetch()

    assert comment.state == PostCommentState.PENDING
    assert comment.post.id == post.id
    assert comment.created_at
    assert comment.modified_at
    assert comment.name == 'Julián'
    assert comment.email == 'anonymous@protonmail.com'


@mark.asyncio
async def test_success_without_name(db_connection):
    post = await PostFactory.create()
    comment = await PostComment.create(
        post=post,
        email='anonymous@protonmail.com',
        body='I like this post'
    )
    comment = await PostComment.get(id=comment.id)
    await comment.post.fetch()

    assert comment.state == PostCommentState.PENDING
    assert comment.post.id == post.id
    assert comment.created_at
    assert comment.modified_at
    assert comment.name == 'anonymous'
    assert comment.email == 'anonymous@protonmail.com'
