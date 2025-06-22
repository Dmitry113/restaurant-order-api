# services/dish_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.models import Dish
from fastapi import HTTPException
from app.schemas.dish import DishCreate



class DishService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_dishes(self):
        result = await self.db.execute(select(Dish))
        return result.scalars().all()

    async def create_dish(self, dish_data: DishCreate):
        dish = Dish(**dish_data.dict())
        self.db.add(dish)
        await self.db.commit()
        await self.db.refresh(dish)
        return dish

    async def delete_dish(self, dish_id: int):
        dish = await self.db.get(Dish, dish_id)
        if not dish:
            raise HTTPException(status_code=404, detail="Dish not found")
        await self.db.delete(dish)
        await self.db.commit()
