from pytest import mark, raises

from raiseexception.blog.controllers import CreatePost
from raiseexception.blog.models import Post
from tests.factories import CategoryFactory


@mark.asyncio
async def test_success(db_connection):
    category = await CategoryFactory.create()
    data = {
        'title': 'test post',
        'body': 'test body',
        'category_id': category.id
    }
    create_post = CreatePost(**data)
    post = await create_post.create()

    assert isinstance(post, Post) is True
    assert post.title == 'test post'
    assert post.body == 'test body'
    assert post.category_id == category.id


missing_data_params = (
    ('title', 'title is obligatory'),
    ('body', 'body is obligatory'),
    ('category_id', 'category_id is obligatory'),
)


@mark.parametrize('field, expected_message', missing_data_params)
@mark.asyncio
async def test_missing_data(field, expected_message, db_connection):
    category = await CategoryFactory.create()
    data = {
        'title': 'test post',
        'body': 'test body',
        'category_id': category.id
    }
    data.pop(field)
    create_post = CreatePost(**data)
    with raises(ValueError) as e:
        await create_post.create()

    assert str(e.value) == expected_message


@mark.asyncio
async def test_category_does_not_exists(db_connection):
    data = {
        'title': 'test post',
        'body': 'test body',
        'category_id': 10000000
    }
    create_post = CreatePost(**data)
    with raises(ValueError) as e:
        await create_post.create()

    assert str(e.value) == 'does not exists category with id: ' \
                           f'{data["category_id"]}'
