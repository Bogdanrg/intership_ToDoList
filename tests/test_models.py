import pytest

from constants import user
from repos.user_repo import UserRepository


@pytest.mark.asyncio
async def test_insert_one_user(async_db_session):
    user_obj = await UserRepository.insert_one(async_db_session, **user)
    await async_db_session.commit()
    assert user_obj.password == user["password"]
    assert user_obj.email == user["email"]


@pytest.mark.asyncio
async def test_insert_without_username(async_db_session):
    user_without_username = {"email": "user@gmil.com", "password": "password"}
    await UserRepository.insert_one(async_db_session, **user_without_username)
    user_obj = await UserRepository.get_user_by_username(
        user["username"], async_db_session
    )
    assert user_obj is None


@pytest.mark.asyncio
async def test_update_one(async_db_session):
    user_obj = await UserRepository.insert_one(async_db_session, **user)
    await async_db_session.commit()
    await UserRepository.update_one(async_db_session, user_obj.id, username="new")
    await async_db_session.commit()
    assert user_obj.username == "new"


@pytest.mark.asyncio
async def test_delete_one(async_db_session):
    user_obj = await UserRepository.insert_one(async_db_session, **user)
    await async_db_session.commit()
    await UserRepository.delete_one(user_obj.id, async_db_session)
    await async_db_session.commit()
    user_obj = await UserRepository.get_user_by_username(
        user["username"], async_db_session
    )
    assert user_obj is None


@pytest.mark.asyncio
async def test_get_user_by_username(async_db_session):
    await UserRepository.insert_one(async_db_session, **user)
    await async_db_session.commit()
    user_obj = await UserRepository.get_user_by_username(
        user["username"], async_db_session
    )
    assert user_obj.password == user["password"]
    assert user_obj.username == user["username"]
