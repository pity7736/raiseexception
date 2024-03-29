from pytest import mark

from raiseexception.blog.constants import PostState
from raiseexception.blog.models import Post


@mark.asyncio
async def test_create(db_connection, user_fixture, category_fixture):
    body = '''
        # post title

        This is the body for the post in markdown format

        - this is a
        - unordered list
        - with three items

        1. And this is a
        1. ordered list
    '''
    await Post.create(
        title='test title',
        body=body,
        category=category_fixture,
        author=user_fixture,
        description='test description'
    )
    post = await Post.get(title='test title')
    await post.category.fetch()

    assert post.id
    assert post.title == 'test title'
    assert post.title_slug == 'test-title'
    assert post.body == body
    assert post.category.name == category_fixture.name
    assert post.created_at
    assert post.modified_at
    assert post.created_at == post.modified_at
    assert post.state == PostState.DRAFT
    assert post.description == 'test description'
