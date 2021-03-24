from tests.factories import CategoryFactory


def test_get(db_connection, event_loop, test_client, cookies_fixture):
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
    assert '<label for="body">Body:</label>' in response.text
    assert '<textarea id="body" name="body" required></textarea>' \
        in response.text
    assert '<input type="submit" value="Create">' in response.text
    assert '<p>post created successfully</p>' not in response.text
    assert '<p></p>' not in response.text


def test_success(db_connection, event_loop, test_client, cookies_fixture):
    category = event_loop.run_until_complete(CategoryFactory.create())
    response = test_client.post(
        '/admin/blog',
        cookies=cookies_fixture,
        data={
            'title': 'test title',
            'body': 'test body',
            'category_id': category.id
        }
    )

    assert response.status_code == 201
    assert '<p>post created successfully</p>' in response.text


def test_missing_data(db_connection, event_loop, test_client, cookies_fixture):
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


def test_with_new_category(db_connection, event_loop, test_client,
                           cookies_fixture):
    response = test_client.post(
        '/admin/blog',
        cookies=cookies_fixture,
        data={
            'title': 'test title',
            'body': 'test body',
            'category_id': 'new category'
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
            'author': '__pity__'
        }
    )

    assert response.status_code == 201
    assert '<p>post created successfully</p>' in response.text
