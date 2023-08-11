import pytest
from httpx import AsyncClient

from base.classes import AsyncSessionManager
from constants import BASE_URL, user
from main import app
from repos.user_repo import UserRepository
from user.service import HasherService


@pytest.mark.asyncio
async def test_registration_route(session_fixture):
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        response = await ac.post("/api/auth/registration/", json=user)
    await UserRepository.delete_one(response.json().get("id"), session_fixture)
    await session_fixture.commit()
    assert response.status_code == 200
    assert set(response.json().keys()) == {"id", "username", "password", "email"}


@pytest.mark.asyncio
async def test_registration_route_without_data():
    user_without_email = {"username": "lolik", "password": "pl,mmkasd"}
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        response = await ac.post("/api/auth/registration/", json=user_without_email)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_route():
    data = {"username": user["username"], "password": user["password"]}
    password_hash = HasherService.get_password_hash(user["password"])
    async with AsyncSessionManager() as session:
        user_obj = await UserRepository.insert_one(
            session,
            password=password_hash,
            username=user["username"],
            email=user["email"],
        )
        await session.commit()
        async with AsyncClient(app=app, base_url=BASE_URL) as ac:
            response = await ac.post("/api/auth/login/", json=data)
        assert response.status_code == 200
        assert set(response.json().keys()) == {"access_token", "refresh_token"}
        await UserRepository.delete_one(user_obj.id, session)
