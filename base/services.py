from fastapi.requests import Request


class AuthService:
    @staticmethod
    def get_token(request: Request) -> str | None:
        token = request.headers.get("JWT")
        return token
