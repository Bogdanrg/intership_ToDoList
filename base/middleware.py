from fastapi import Request
from fastapi.responses import JSONResponse

from base.classes import AsyncSessionManager
from repos.user_repo import UserRepository
from user.service import JWTService

from .services import AuthMiddlewareService


class AuthMiddleware:
    async def __call__(self, request: Request, call_next) -> JSONResponse:
        if not AuthMiddlewareService.is_safe_path(request):
            async with AsyncSessionManager() as session:
                token = AuthMiddlewareService.get_token(request)
                if not token:
                    return JSONResponse(
                        content="Token wasn't provided", status_code=400
                    )
                payload = await JWTService.decode_token(token)
                if not payload:
                    return JSONResponse(content="Invalid token", status_code=400)
                user = await UserRepository.get_user_by_username(
                    payload.get("username", ""), session
                )
                if not user:
                    return JSONResponse(content="Invalid token", status_code=400)
                request.state.user = user
                response = await call_next(request)
                return response
        response = await call_next(request)
        return response
