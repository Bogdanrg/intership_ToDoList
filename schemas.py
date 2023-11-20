from pydantic import BaseModel


class PhoneModel(BaseModel):
    id: str
    name: str
    price: float
    onMarket: bool
    description: str
    count: int


class FoodModel(BaseModel):
    id: str
    name: str
    calories: float
    description: str
    count: int
