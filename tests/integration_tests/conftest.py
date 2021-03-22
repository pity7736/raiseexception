import os
from unittest.mock import AsyncMock, patch

import asyncpg
from asyncpg import Pool, Connection
from asyncpg.transaction import Transaction
from pytest import fixture
from starlette.testclient import TestClient

from raiseexception import settings, app
from tests.factories import UserFactory

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


@fixture(scope='session')
def schema():
    with open(f'{CURRENT_DIR}/db.sql') as f:
        result = f.read()
    return result


@fixture(scope='session')
async def db_pool(session_mocker):
    print(f'connecting to {settings.DB_NAME} database'.upper())
    pool: Pool = await asyncpg.create_pool(
        host=settings.DB_HOST,
        user=settings.DB_USER,
        database=settings.DB_NAME,
        password=settings.DB_PASSWORD,
        port=int(settings.DB_PORT),
        min_size=2
    )
    print('pool created')
    pool_mock = session_mocker.patch.object(
        asyncpg,
        'create_pool',
        new_callable=AsyncMock
    )
    pool_mock.return_value = pool
    yield pool
    print('closing pool')
    await pool.close()
    print('pool closed')


@fixture
async def db_connection(db_pool, schema, mocker):
    connection: Connection = await db_pool.acquire()
    transaction: Transaction = connection.transaction()
    await transaction.start()
    connect_mock = mocker.patch.object(
        asyncpg,
        'connect',
        new_callable=AsyncMock
    )
    connect_mock.return_value = connection
    close_mock = patch.object(Connection, 'close', new_callable=AsyncMock)
    close_mock.start()
    await connection.execute(schema)
    yield connection
    print('doing rollback')
    await transaction.rollback()
    print('rollback done!')
    print('releasing connection')
    close_mock.stop()
    await db_pool.release(connection)


@fixture
def test_client():
    return TestClient(app=app)


@fixture
def cookies_fixture(event_loop, test_client):
    user = event_loop.run_until_complete(UserFactory.create())
    login_response = test_client.post(
        '/auth/login',
        data={'username': user.username, 'password': UserFactory.password}
    )
    return login_response.cookies.get_dict()
