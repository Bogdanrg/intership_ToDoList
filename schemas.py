from decimal import Decimal

from pydantic import BaseModel


class PhoneModel(BaseModel):
    id: str
    name: str
    price: Decimal
    onMarket: bool
    description: str
    count: int


class FoodModel(BaseModel):
    id: str
    name: str
    calories: Decimal
    description: str
    count: int
