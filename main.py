from fastapi import FastAPI
from config import settings
from api.api_routes import api_router


app = FastAPI(title=settings.app.TITLE)

app.include_router(api_router)
