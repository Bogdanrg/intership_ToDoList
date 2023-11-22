from typing import List

from fastapi import APIRouter
from schemas import PhoneModel, FoodModel
from analytical_service.services import AnalyticalServices


analytical_router = APIRouter(prefix="/analyze", tags=["analytical_service"])


@analytical_router.get("/most_popular_phone", response_model=PhoneModel)
async def get_most_popular_phone_doc() -> dict:
    phone_document = await AnalyticalServices.get_the_most_popular_phone()
    return phone_document


@analytical_router.get("/most_popular_food", response_model=FoodModel)
async def get_most_popular_food_doc() -> dict:
    food_document = await AnalyticalServices.get_the_most_popular_food()
    return food_document


@analytical_router.get("/phones", response_model=List[PhoneModel])
async def get_phone_documents(page: int, limit: int) -> List[dict]:
    phone_list = await AnalyticalServices.get_phone_list(page, limit)
    return phone_list


@analytical_router.get("/food", response_model=List[FoodModel])
async def get_food_documents(page: int, limit: int) -> List[dict]:
    food_list = await AnalyticalServices.get_food_list(page, limit)
    return food_list
