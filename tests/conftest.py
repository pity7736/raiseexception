import asyncio

import uvloop
from pytest import fixture


@fixture(scope='session')
def event_loop():
    uvloop.install()
    return asyncio.get_event_loop()
