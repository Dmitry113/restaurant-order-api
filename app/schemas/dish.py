# schemas/dish.py
from pydantic import BaseModel, Field
from typing import Optional


class DishBase(BaseModel):
    name: str
    description: str
    price: float = Field(..., gt=0)
    category: str


class DishCreate(DishBase):
    pass


class DishRead(DishBase):
    id: int

    model_config = {
        "from_attributes": True
    }

