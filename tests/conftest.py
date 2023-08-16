import asyncio

import pytest
import pytest_asyncio
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession

from base.classes import AsyncSessionManager
from core.database import async_session, engine
from user.service import JWTService


@pytest_asyncio.fixture(scope="function")
async def async_db_session():
    connection = await engine.connect()
    trans = await connection.begin()
    session = async_session(bind=connection)
    nested = await connection.begin_nested()

    @event.listens_for(session.sync_session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested

        if not nested.is_active:
            nested = connection.sync_connection.begin_nested()

    yield session

    await trans.rollback()
    await session.close()
    await connection.close()


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def session_fixture() -> AsyncSession:
    async with AsyncSessionManager() as session:
        yield session


@pytest.fixture
async def access_token() -> str:
    access_token = await JWTService.encode_access_token("Bogdan")
    yield access_token
    del access_token


@pytest.fixture
def user() -> dict:
    return {"username": "Bogdan", "password": "password", "email": "user@gmail.com"}

