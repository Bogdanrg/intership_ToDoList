import re

from fastapi.requests import Request
from fastapi.responses import JSONResponse

from constants import AUTH_SAFE_PATHS


class AuthMiddlewareService:
    @staticmethod
    def get_token(request: Request) -> str | JSONResponse:
        token = request.headers.get("JWT")
        return token

    @staticmethod
    def is_safe_path(request: Request) -> bool:
        if (
            re.search(r"http://127.0.0.1:8000/docs\S+", str(request.url))
            or str(request.url) in AUTH_SAFE_PATHS
        ):
            return True
        return False
