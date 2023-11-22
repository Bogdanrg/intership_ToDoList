from fastapi import APIRouter
from api.v1.analyze.analytical_routes import analytical_router


v1_router = APIRouter(prefix="/v1")
v1_router.include_router(analytical_router)
