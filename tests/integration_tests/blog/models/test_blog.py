from pytest import mark

from raiseexception.blog.models import Category, Post


@mark.asyncio
async def test_success(db_connection):
    category = await Category.create(name='test name')
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
        category=category
    )
    post = await Post.get(title='test title')
    await post.category.fetch()

    assert post.id
    assert post.title == 'test title'
    assert post.body == body
    assert post.category.name == 'test name'
