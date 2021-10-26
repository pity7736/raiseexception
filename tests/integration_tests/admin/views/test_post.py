import datetime

from pytest import mark

from raiseexception.blog.constants import PostState
from raiseexception.blog.models import Post
from raiseexception.mailing.client import MailClient
from tests.factories import CategoryFactory, PostFactory, SubscriptionFactory


def test_get_posts(db_connection, event_loop, test_client, cookies_fixture):
    category1, category2, category3 = event_loop.run_until_complete(
        CategoryFactory.create_batch(3)
    )
    response = test_client.get('/admin/blog', cookies=cookies_fixture)

    assert response.status_code == 200
    assert '<form id="create-post" action="/admin/blog" method="post">' \
        in response.text
    assert '<label for="title">Title:</label>' in response.text
    assert '<input id="title" name="title" type="text" required autofocus>' \
        in response.text
    assert '<label for="category_id">Category:</label>' in response.text
    assert '<input id="category_id" name="category_id" list="category_values' \
           '" required>' in response.text
    assert '<datalist id="category_values">' in response.text
    assert f'<option value="{category1.id}">{category1.name}</option>' \
        in response.text
    assert f'<option value="{category2.id}">{category2.name}</option>' \
        in response.text
    assert f'<option value="{category3.id}">{category3.name}</option>' \
        in response.text
    assert '</datalist>' in response.text
    assert '<label for="description">Description:</label>' in response.text
    assert '<input id="description" name="description" type="text" required>' \
        in response.text
    assert '<label for="body">Body:</label>' in response.text
    assert '<textarea id="body" name="body" required></textarea>' \
        in response.text
    assert '<input type="submit" value="Create">' in response.text
    assert '<p>post created successfully</p>' not in response.text


def test_create_post(db_connection, event_loop, test_client, cookies_fixture):
    category = event_loop.run_until_complete(CategoryFactory.create())
    response = test_client.post(
        '/admin/blog',
        cookies=cookies_fixture,
        data={
            'title': 'test title',
            'body': 'test body',
            'category_id': category.id,
            'description': 'test description'
        }
    )

    assert response.status_code == 201
    assert '<p>post created successfully</p>' in response.text


def test_create_post_with_missing_data(db_connection, event_loop, test_client,
                                       cookies_fixture):
    category = event_loop.run_until_complete(CategoryFactory.create())
    response = test_client.post(
        '/admin/blog',
        cookies=cookies_fixture,
        data={
            'body': 'test body',
            'category_id': category.id
        }
    )

    assert response.status_code == 400
    assert '<p>title is obligatory</p>' in response.text


def test_create_post_with_new_category(db_connection, event_loop, test_client,
                                       cookies_fixture):
    response = test_client.post(
        '/admin/blog',
        cookies=cookies_fixture,
        data={
            'title': 'test title',
            'body': 'test body',
            'category_id': 'new category',
            'description': 'test description'
        }
    )

    assert response.status_code == 201
    assert '<p>post created successfully</p>' in response.text


def test_send_author_field(db_connection, event_loop, test_client,
                           cookies_fixture):
    response = test_client.post(
        '/admin/blog',
        cookies=cookies_fixture,
        data={
            'title': 'test title',
            'body': 'test body',
            'category_id': 'new category',
            'author': '__pity__',
            'description': 'test description'
        }
    )

    assert response.status_code == 201
    assert '<p>post created successfully</p>' in response.text


def test_get_post(db_connection, event_loop, test_client, cookies_fixture):
    category1, category2, category3 = event_loop.run_until_complete(
        CategoryFactory.create_batch(3)
    )
    post = event_loop.run_until_complete(PostFactory.create())
    response = test_client.get(
        f'/admin/blog/{post.title_slug}',
        cookies=cookies_fixture
    )

    assert response.status_code == 200
    assert '<form id="update-post" method="post">' \
        in response.text
    assert '<label for="title">Title:</label>' in response.text
    assert f'<input id="title" name="title" type="text" required autofocus ' \
           f'value="{post.title}">' in response.text
    assert '<label for="category_id">Category:</label>' in response.text
    assert '<input id="category_id" name="category_id" list="category_values' \
           f'" required value="{post.category_id}">' in response.text
    assert '<datalist id="category_values">' in response.text
    assert f'<option value="{category1.id}">{category1.name}</option>' \
        in response.text
    assert f'<option value="{category2.id}">{category2.name}</option>' \
        in response.text
    assert f'<option value="{category3.id}">{category3.name}</option>' \
        in response.text
    assert '</datalist>' in response.text
    assert '<label for="description">Description:</label>' in response.text
    assert '<input id="description" name="description" type="text" required ' \
           f'value="{post.description}">' in response.text
    assert '<label for="body">Body:</label>' in response.text
    assert '<textarea id="body" name="body" required>' \
           f'{post.body}</textarea>' in response.text
    assert '<input type="submit" value="Update">' in response.text
    assert '<p>post updated successfully</p>' not in response.text


post_data_params = (
    (
        {
            'state': PostState.PUBLISHED.value
        }
    ),
    (
        {
            'title': 'New post title'
        }
    ),
    (
        {
            'state': PostState.PUBLISHED.value,
            'title': 'New post title'
        }
    ),
    (
        {
            'body': 'new post body'
        }
    ),
    (
        {
            'description': 'new post description'
        }
    ),
)


@mark.parametrize('post_data', post_data_params)
def test_update_post(db_connection, event_loop, test_client, cookies_fixture,
                     post_data):
    post = event_loop.run_until_complete(PostFactory.create())
    response = test_client.post(
        f'/admin/blog/{post.title_slug}',
        cookies=cookies_fixture,
        data=post_data
    )
    updated_post = event_loop.run_until_complete(Post.get(id=post.id))

    assert response.status_code == 200
    assert post.modified_at != updated_post.modified_at
    if 'state' in post_data:
        assert updated_post.state != post.state
        assert updated_post.state == PostState(post_data['state'])
    if 'title' in post_data:
        assert updated_post.title != post.title
        assert updated_post.title_slug != post.title_slug
        assert updated_post.title == post_data['title']
    if 'body' in post_data:
        assert updated_post.body != post.body
        assert updated_post.body == post_data['body']
    if 'description' in post_data:
        assert updated_post.description != post.description
        assert updated_post.description == post_data['description']
    assert '<p>post updated successfully</p>' in response.text


def test_update_post_with_wrong_field(db_connection, event_loop, test_client,
                                      cookies_fixture):
    post = event_loop.run_until_complete(PostFactory.create())
    response = test_client.post(
        f'/admin/blog/{post.title_slug}',
        cookies=cookies_fixture,
        data={'wrong_field': 'value'}
    )
    assert response.status_code == 400
    assert '<p>"wrong_field" is an invalid field</p>'


def test_publish_post(db_connection, event_loop, test_client, cookies_fixture,
                      mocker):
    post = event_loop.run_until_complete(PostFactory.create())
    event_loop.run_until_complete(SubscriptionFactory.create(verified=True))
    mail_client_spy = mocker.spy(MailClient, 'send')
    response = test_client.post(
        '/admin/blog/publish',
        cookies=cookies_fixture,
        data={'post_id': post.id}
    )
    published_post = event_loop.run_until_complete(Post.get(id=post.id))

    assert response.status_code == 302
    assert published_post.state == PostState.PUBLISHED
    assert published_post.published_at.date() == datetime.date.today()
    mail_client_spy.assert_called_once()


def test_publish_post_with_many_subscribers(
        db_connection,
        event_loop,
        test_client,
        cookies_fixture,
        mocker):
    post = event_loop.run_until_complete(PostFactory.create())
    event_loop.run_until_complete(SubscriptionFactory.create_batch(
        size=5,
        verified=True
    ))
    mail_client_spy = mocker.spy(MailClient, 'send')
    response = test_client.post(
        '/admin/blog/publish',
        cookies=cookies_fixture,
        data={'post_id': post.id}
    )
    published_post = event_loop.run_until_complete(Post.get(id=post.id))

    assert response.status_code == 302
    assert published_post.state == PostState.PUBLISHED
    assert published_post.published_at.date() == datetime.date.today()
    assert mail_client_spy.call_count == 5


def test_publish_post_with_many_subscribers_and_some_not_verified(
        db_connection,
        event_loop,
        test_client,
        cookies_fixture,
        mocker):
    post = event_loop.run_until_complete(PostFactory.create())
    event_loop.run_until_complete(SubscriptionFactory.create_batch(
        size=3,
        verified=True
    ))
    event_loop.run_until_complete(SubscriptionFactory.create_batch(size=3))
    mail_client_spy = mocker.spy(MailClient, 'send')
    response = test_client.post(
        '/admin/blog/publish',
        cookies=cookies_fixture,
        data={'post_id': post.id}
    )
    published_post = event_loop.run_until_complete(Post.get(id=post.id))

    assert response.status_code == 302
    assert published_post.state == PostState.PUBLISHED
    assert published_post.published_at.date() == datetime.date.today()
    assert mail_client_spy.call_count == 3
