from unittest.mock import AsyncMock

import asyncpg
from asyncpg import Pool, Connection
from asyncpg.transaction import Transaction
from pytest import fixture

from raiseexception import settings


@fixture(scope='session')
async def db_pool(session_mocker):
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
async def db_connection(db_pool):
    connection: Connection = await db_pool.acquire()
    transaction: Transaction = connection.transaction()
    await transaction.start()
    yield connection
    print('doing rollback')
    await transaction.rollback()
    print('rollback done!')
    print('releasing connection')
    await db_pool.release(connection)
