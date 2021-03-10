from pytest import mark


@mark.asyncio
async def test_create_user(db_connection):
    print(db_connection)
    users = await db_connection.fetch('select * from users')
    print(users)
