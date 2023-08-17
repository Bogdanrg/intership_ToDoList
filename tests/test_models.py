import pytest
import sqlalchemy

from repos.task_list_repo import TaskListRepository
from repos.task_repo import TaskRepository
from repos.user_repo import UserRepository


@pytest.mark.asyncio
async def test_insert_one_user(async_db_session, user):
    # Act
    user_obj = await UserRepository.insert_one(async_db_session, **user)
    await async_db_session.commit()
    # Assert
    assert user_obj.password == user["password"]
    assert user_obj.email == user["email"]


@pytest.mark.asyncio
async def test_insert_without_username(async_db_session, user):
    # Arrange
    user_without_username = {"email": "user@gmil.com", "password": "password"}
    # Act
    try:
        await UserRepository.insert_one(async_db_session, **user_without_username)
        await async_db_session.flush()
    except sqlalchemy.exc.IntegrityError:
        await async_db_session.rollback()
    user_obj = await UserRepository.get_user_by_username(
        user["username"], async_db_session
    )
    # Assert
    assert user_obj is None


@pytest.mark.asyncio
async def test_update_one(async_db_session, user):
    # Act
    user_obj = await UserRepository.insert_one(async_db_session, **user)
    await async_db_session.commit()
    await UserRepository.update_one(async_db_session, user_obj.id, username="new")
    await async_db_session.commit()
    # Assert
    assert user_obj.username == "new"


@pytest.mark.asyncio
async def test_delete_one(async_db_session, user):
    # Act
    user_obj = await UserRepository.insert_one(async_db_session, **user)
    await async_db_session.commit()
    await UserRepository.delete_one(user_obj.id, async_db_session)
    await async_db_session.commit()
    user_obj = await UserRepository.get_user_by_username(
        user["username"], async_db_session
    )
    # Assert
    assert user_obj is None


@pytest.mark.asyncio
async def test_get_user_by_username(async_db_session, user):
    # Act
    await UserRepository.insert_one(async_db_session, **user)
    await async_db_session.commit()
    user_obj = await UserRepository.get_user_by_username(
        user["username"], async_db_session
    )
    # Assert
    assert user_obj.password == user["password"]
    assert user_obj.username == user["username"]


@pytest.mark.asyncio
async def test_get_task_list_by_name_and_user(async_db_session, user):
    # Act
    user_obj = await UserRepository.insert_one(async_db_session, **user)
    await TaskListRepository.insert_one(
        async_db_session, name="task_list", user=user_obj
    )
    await async_db_session.commit()
    task_list_obj = await TaskListRepository.get_task_list_by_name_and_user(
        async_db_session, "task_list", user_obj
    )
    # Assert
    assert task_list_obj.name == "task_list"
    assert task_list_obj.user_id == user_obj.id


@pytest.mark.asyncio
async def test_get_task_list_by_another_user(async_db_session, user):
    # Act
    user_obj = await UserRepository.insert_one(async_db_session, **user)
    user_another_obj = await UserRepository.insert_one(
        async_db_session, username="abc", email="email", password="hey"
    )
    await TaskListRepository.insert_one(
        async_db_session, name="task_list", user=user_obj
    )
    await async_db_session.commit()
    task_list_obj = await TaskListRepository.get_task_list_by_name_and_user(
        async_db_session, "task_list", user_another_obj
    )
    # Assert
    assert task_list_obj is None


@pytest.mark.asyncio
async def test_get_task_by_name_and_list(async_db_session, user):
    # Act
    user_obj = await UserRepository.insert_one(async_db_session, **user)

    task_list_obj = await TaskListRepository.insert_one(
        async_db_session, name="task_list", user=user_obj
    )
    await TaskRepository.insert_one(
        async_db_session, name="abc", content="content", list=task_list_obj
    )
    await async_db_session.commit()
    task_obj = await TaskRepository.get_task_by_name_and_list(
        async_db_session, "abc", task_list_obj
    )
    # Assert
    assert task_obj.name == "abc"
    assert task_obj.content == "content"
    assert task_obj.list_id == task_list_obj.id


@pytest.mark.asyncio
async def test_get_task_by_name_and_wrong_list(async_db_session, user):
    # Act
    user_obj = await UserRepository.insert_one(async_db_session, **user)

    task_list_obj = await TaskListRepository.insert_one(
        async_db_session, name="task_list", user=user_obj
    )
    task_list_another_obj = await TaskListRepository.insert_one(
        async_db_session, name="new_task", user=user_obj
    )
    await TaskRepository.insert_one(
        async_db_session, name="abc", content="content", list=task_list_obj
    )
    await async_db_session.commit()
    task_obj = await TaskRepository.get_task_by_name_and_list(
        async_db_session, "abc", task_list_another_obj
    )
    # Assert
    assert task_obj is None
