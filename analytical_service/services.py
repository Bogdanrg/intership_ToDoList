from typing import List

from repos.food_repo import FoodRepository
from repos.phone_repo import PhoneRepository
from schemas import PhoneModel, FoodModel


class AnalyticalServices:

    @staticmethod
    async def create_food_document(data: dict) -> None:
        await FoodRepository.create(data)

    @staticmethod
    async def create_phone_document(data: dict) -> None:
        await PhoneRepository.create(data)

    @staticmethod
    async def search_food_document(data: dict) -> None:
        await FoodRepository.increase_count(data.get("id"))

    @staticmethod
    async def search_phone_document(data: dict) -> None:
        print(data)
        await PhoneRepository.increase_count(data.get("id"))

    @staticmethod
    async def get_the_most_popular_phone() -> dict:
        phones = await PhoneRepository.get_all()
        phone = phones[0]
        return phone

    @staticmethod
    async def get_the_most_popular_food() -> dict:
        food = await FoodRepository.get_all()
        food = food[0]
        return food

    @staticmethod
    async def get_phone_list() -> List[dict]:
        phone_list = await PhoneRepository.get_all()
        return phone_list

    @staticmethod
    async def get_food_list() -> List[dict]:
        food_list = await FoodRepository.get_all()
        return food_list
