from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_session
from app.schemas.order import OrderCreate, OrderRead, OrderStatusUpdate
from app.services.order_service import OrderService

router = APIRouter(tags=["Заказы"])


@router.get("/", response_model=List[OrderRead])
async def get_orders(session: AsyncSession = Depends(get_session)):
    service = OrderService(session)
    return await service.get_all_orders()


@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreate, session: AsyncSession = Depends(get_session)):
    service = OrderService(session)
    return await service.create_order(order_data)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int, session: AsyncSession = Depends(get_session)):
    service = OrderService(session)
    await service.delete_order(order_id)


@router.patch("/{order_id}/status", response_model=OrderRead)
async def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    session: AsyncSession = Depends(get_session),
):
    service = OrderService(session)
    return await service.update_order_status(order_id, status_update.status)
