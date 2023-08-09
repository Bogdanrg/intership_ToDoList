from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query, dependencies
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from base.classes import AsyncSessionManager
from core.database import engine
from repos.user_repo import UserRepository
from schemas import SignInModel, SignUpModel, TokenPairModel
from user.service import HasherService, JWTService

auth_router = APIRouter(prefix="/api/auth", tags=["auth"])


@auth_router.post("/registration/")
async def register_user(user: SignUpModel) -> Any:
    async with AsyncSessionManager() as session:
        await UserRepository.insert_one(
            session,
            username=user.username,
            email=user.email,
            password=HasherService.get_password_hash(user.password),
        )
    return "Created"


@auth_router.put(
    "/change-username/", dependencies=[Depends(JWTService.login_required)]
)
async def update_username(
    username: Annotated[str | None, Query(max_length=100)] = "new_username",
) -> Any:
    async with AsyncSession(engine) as session, session.begin():
        await UserRepository.update_one(session, 1, username=username)
    return "Updated"


@auth_router.post("/login/", response_model=TokenPairModel)
async def login_user(user: SignInModel) -> Any:
    async with AsyncSession(engine) as session, session.begin():
        is_valid_user = await JWTService.check_credentials(
            session, user.username, user.password
        )
        if not is_valid_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid username or password",
            )
        jwt_pair = await JWTService.get_token_pair(user.username)
        return jwt_pair


@auth_router.post("/refresh/", response_model=TokenPairModel)
async def refresh_access_token(refresh_token: str) -> Any:
    async with AsyncSession(engine) as session, session.begin():
        tokens = await JWTService.refresh_access_token(session, refresh_token)
        if not tokens:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid refresh token"
            )
        return tokens
