from pytest import mark, raises

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


invalid_email_params = (
    'wrong email',
    'wrong@email',

)


@mark.parametrize('email', invalid_email_params)
@mark.asyncio
async def test_create_with_wrong_email(email, db_connection):
    with raises(ValueError):
        await PostComment.create(email=email)


@mark.asyncio
async def test_get_comment_with_none_email(db_connection):
    post = await PostFactory.create()
    await PostComment.create(
        post=post,
        body='body',
    )

    comment = await PostComment.get()

    assert comment.post_id == post.id
    assert comment.body == 'body'
    assert comment.email is None


@mark.asyncio
async def test_get_comment_with_empty_email(db_connection):
    post = await PostFactory.create()
    await PostComment.create(
        post=post,
        body='body',
        email=''
    )

    comment = await PostComment.get()

    assert comment.post_id == post.id
    assert comment.body == 'body'
    assert comment.email == ''
