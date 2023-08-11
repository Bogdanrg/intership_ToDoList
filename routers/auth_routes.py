from typing import Any

from fastapi import APIRouter, HTTPException, Request
from starlette import status

from base.classes import AsyncSessionManager
from repos.user_repo import UserRepository
from schemas import SignInModel, SignUpModel, TokenPairModel
from user.service import HasherService, JWTService

auth_router = APIRouter(prefix="/api/auth", tags=["auth"])


@auth_router.post("/registration/", response_model=SignUpModel)
async def register_user(user: SignUpModel) -> Any:
    async with AsyncSessionManager() as session:
        user = await UserRepository.insert_one(
            session,
            username=user.username,
            email=user.email,
            password=HasherService.get_password_hash(user.password),
        )
    return user


@auth_router.post("/login/", response_model=TokenPairModel)
async def login_user(user: SignInModel) -> Any:
    async with AsyncSessionManager() as session:
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
async def refresh_access_token(request: Request) -> Any:
    token = request.headers.get("JWT")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Token wasn't provided"
        )
    async with AsyncSessionManager() as session:
        tokens = await JWTService.refresh_access_token(session, token)
        if not tokens:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid refresh token"
            )
        return tokens
