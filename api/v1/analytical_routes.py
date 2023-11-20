from fastapi import APIRouter
from schemas import PhoneModel, FoodModel
from analytical_service.services import AnalyticalServices


analytical_router = APIRouter(prefix="/api/v1/analyze", tags=["analytical_service"])


@analytical_router.get("/most_popular_phone", response_model=PhoneModel)
async def get_most_popular_phone_doc() -> dict:
    phone_document = await AnalyticalServices.get_the_most_popular_phone()
    return phone_document


@analytical_router.get("/most_popular_food", response_model=FoodModel)
async def get_most_popular_food_doc() -> dict:
    food_document = await AnalyticalServices.get_the_most_popular_food()
    return food_document
