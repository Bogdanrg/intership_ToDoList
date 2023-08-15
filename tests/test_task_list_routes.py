import pytest
from httpx import AsyncClient

from constants import BASE_URL, user
from main import app
from repos.task_list_repo import TaskListRepository
from repos.task_repo import TaskRepository
from repos.user_repo import UserRepository


@pytest.mark.asyncio
async def test_create_task_list(session_fixture, access_token):
    data = {"name": "abc"}
    headers = {"JWT": access_token}
    user_obj = await UserRepository.insert_one(session_fixture, **user)
    await session_fixture.commit()
    async with AsyncClient(app=app, base_url=BASE_URL, headers=headers) as ac:
        response = await ac.post("/api/v1/task_list/", json=data)
    await TaskListRepository.delete_one(response.json().get("id"), session_fixture)
    await UserRepository.delete_one(user_obj.id, session_fixture)
    await session_fixture.commit()
    assert response.status_code == 200
    assert set(response.json().keys()) == {"id", "name", "active_date"}


@pytest.mark.asyncio
async def test_get_wrong_task_list(session_fixture, access_token):
    headers = {"JWT": access_token}
    user_obj = await UserRepository.insert_one(session_fixture, **user)
    await session_fixture.commit()
    async with AsyncClient(app=app, base_url=BASE_URL, headers=headers) as ac:
        response = await ac.get("/api/v1/task_list/my_list/")
    await UserRepository.delete_one(user_obj.id, session_fixture)
    await session_fixture.commit()
    assert response.status_code == 400
    assert response.content == b'{"detail":"You have no lists with the name"}'


@pytest.mark.asyncio
async def test_get_task_list(session_fixture, access_token):
    data = {"name": "abc", "content": "do it"}
    headers = {"JWT": access_token}
    user_obj = await UserRepository.insert_one(session_fixture, **user)
    task_list_obj = await TaskListRepository.insert_one(
        session_fixture, name="list", user=user_obj
    )
    task_obj = await TaskRepository.insert_one(
        session_fixture, **data, list=task_list_obj
    )
    await session_fixture.commit()
    async with AsyncClient(app=app, base_url=BASE_URL, headers=headers) as ac:
        response = await ac.get("/api/v1/task_list/list/")
    await TaskRepository.delete_one(task_obj.id, session_fixture)
    await TaskListRepository.delete_one(task_list_obj.id, session_fixture)
    await UserRepository.delete_one(user_obj.id, session_fixture)
    await session_fixture.commit()
    assert response.status_code == 200
    assert set(response.json()[0].keys()) == {"id", "name", "content", "list_id"}


@pytest.mark.asyncio
async def test_add_task(session_fixture, access_token):
    data = {"name": "abc", "content": "do it"}
    headers = {"JWT": access_token}
    user_obj = await UserRepository.insert_one(session_fixture, **user)
    task_list_obj = await TaskListRepository.insert_one(
        session_fixture, name="list", user=user_obj
    )
    await session_fixture.commit()
    async with AsyncClient(app=app, base_url=BASE_URL, headers=headers) as ac:
        response = await ac.post("/api/v1/task_list/list/add/", json=data)
    await TaskRepository.delete_one(response.json().get("id"), session_fixture)
    await TaskListRepository.delete_one(task_list_obj.id, session_fixture)
    await UserRepository.delete_one(user_obj.id, session_fixture)
    await session_fixture.commit()
    assert response.status_code == 200
    assert set(response.json().keys()) == {"id", "name", "content", "list_id"}


@pytest.mark.asyncio
async def test_delete_wrong_task(session_fixture, access_token):
    data = {"name": "abc", "content": "do it"}
    headers = {"JWT": access_token}
    user_obj = await UserRepository.insert_one(session_fixture, **user)
    task_list_obj = await TaskListRepository.insert_one(
        session_fixture, name="list", user=user_obj
    )
    task_obj = await TaskRepository.insert_one(
        session_fixture, **data, list=task_list_obj
    )
    await session_fixture.commit()
    async with AsyncClient(app=app, base_url=BASE_URL, headers=headers) as ac:
        response = await ac.delete("/api/v1/task_list/list/delete/mytask/")
    await TaskRepository.delete_one(task_obj.id, session_fixture)
    await TaskListRepository.delete_one(task_list_obj.id, session_fixture)
    await UserRepository.delete_one(user_obj.id, session_fixture)
    await session_fixture.commit()
    assert response.status_code == 400
    assert (
        response.content == b'{"detail":"You have no tasks with the name in that list"}'
    )


@pytest.mark.asyncio
async def test_delete_task(session_fixture, access_token):
    data = {"name": "abc", "content": "do it"}
    headers = {"JWT": access_token}
    user_obj = await UserRepository.insert_one(session_fixture, **user)
    task_list_obj = await TaskListRepository.insert_one(
        session_fixture, name="list", user=user_obj
    )
    await TaskRepository.insert_one(session_fixture, **data, list=task_list_obj)
    await session_fixture.commit()
    async with AsyncClient(app=app, base_url=BASE_URL, headers=headers) as ac:
        response = await ac.delete("/api/v1/task_list/list/delete/abc/")
    await TaskListRepository.delete_one(task_list_obj.id, session_fixture)
    await UserRepository.delete_one(user_obj.id, session_fixture)
    await session_fixture.commit()
    assert response.status_code == 200
    assert response.json() == "Deleted"
