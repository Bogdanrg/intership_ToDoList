import pytest
from httpx import AsyncClient

from base.classes import AsyncSessionManager
from constants import BASE_URL
from main import app
from repos.user_repo import UserRepository
from user.service import HasherService


@pytest.mark.asyncio
async def test_registration_route(session_fixture, user):
    # Act
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        response = await ac.post("/api/auth/registration/", json=user)
    await UserRepository.delete_one(response.json().get("id"), session_fixture)
    await session_fixture.commit()
    # Assert
    assert response.status_code == 200
    assert set(response.json().keys()) == {"id", "username", "password", "email"}


@pytest.mark.asyncio
async def test_registration_route_without_data():
    # Arrange
    user_without_email = {"username": "lolik", "password": "pl,mmkasd"}
    # Act
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        response = await ac.post("/api/auth/registration/", json=user_without_email)
    # Assert
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_route(user):
    # Arrange
    data = {"username": user["username"], "password": user["password"]}
    password_hash = HasherService.get_password_hash(user["password"])
    # Act
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
        # Assert
        assert response.status_code == 200
        assert set(response.json().keys()) == {"access_token", "refresh_token"}
        await UserRepository.delete_one(user_obj.id, session)
