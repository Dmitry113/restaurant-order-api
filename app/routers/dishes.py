# routers/dishes.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.services.dish_service import DishService
from app.schemas.dish import DishCreate, DishRead

router = APIRouter(tags=["Блюда"])


@router.get("/", response_model=list[DishRead])
async def get_dishes(session: AsyncSession = Depends(get_session)):
    service = DishService(session)
    return await service.get_all_dishes()


@router.post("/", response_model=DishRead, status_code=status.HTTP_201_CREATED)
async def create_dish(dish: DishCreate, session: AsyncSession = Depends(get_session)):
    service = DishService(session)
    return await service.create_dish(dish)


@router.delete("/{dish_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dish(dish_id: int, session: AsyncSession = Depends(get_session)):
    service = DishService(session)
    await service.delete_dish(dish_id)
