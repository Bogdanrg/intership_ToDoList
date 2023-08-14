import pytest
from httpx import AsyncClient

from constants import BASE_URL
from main import app
from repos.task_list_repo import TaskListRepository


@pytest.mark.asyncio
async def test_create_task_list(async_db_session, session_fixture):
    # user_obj = await UserRepository.insert_one(session_fixture, **user)
    data = {"name": "abc", "user_id": ...}
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        response = await ac.post("/api/v1/task_list/", json=data)
    await TaskListRepository.delete_one(response.json().get("id"), session_fixture)
    await session_fixture.commit()
    assert response.status_code == 200
    assert set(response.json().keys()) == {"id", "name", "active_date", "user_id"}
