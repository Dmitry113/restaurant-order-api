from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

# Связь "блюдо + количество"
class OrderDishCreate(BaseModel):
    dish_id: int
    quantity: int = Field(gt=0, description="Количество должно быть больше нуля")


# Для чтения вложенного блюда в заказе
class OrderDishRead(BaseModel):
    dish_id: int
    name: str
    quantity: int

    class Config:
        orm_mode = True


# Создание заказа
class OrderCreate(BaseModel):
    customer_name: str
    dishes: List[OrderDishCreate]


# Ответ при чтении заказа
class OrderRead(BaseModel):
    id: int
    customer_name: str
    order_time: datetime
    status: str
    dishes: List[OrderDishRead]

    class Config:
        orm_mode = True


# Изменение статуса заказа
class OrderStatusUpdate(BaseModel):
    status: str = Field(..., description="Новый статус заказа (например, готовится)")
