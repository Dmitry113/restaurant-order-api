from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from fastapi import HTTPException, status
from typing import List

from app.models import Order, Dish, OrderDish
from app.schemas.order import OrderCreate
from app.utils.logger import logger


class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_orders(self) -> List[Order]:
        """
        Получить список всех заказов с блюдами (с использованием joinedload для избежания N+1)
        """
        logger.info("Получение всех заказов")
        result = await self.session.execute(
            select(Order).options(joinedload(Order.dishes).joinedload(OrderDish.dish))
        )
        return result.scalars().all()

    async def create_order(self, order_data: OrderCreate) -> Order:
        """
        Создать новый заказ с проверкой существования блюд.
        Изначально статус = 'в обработке'.
        """
        logger.info(f"Создание нового заказа от клиента '{order_data.customer_name}'")

        if not order_data.dishes:
            logger.warning("Попытка создать заказ без блюд")
            raise HTTPException(status_code=400, detail="Заказ должен содержать хотя бы одно блюдо")

        dish_ids = [item.dish_id for item in order_data.dishes]
        result = await self.session.execute(select(Dish).where(Dish.id.in_(dish_ids)))
        dishes = result.scalars().all()

        if len(dishes) != len(dish_ids):
            logger.warning("Некоторые блюда из заказа не существуют")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Один или несколько указанных блюд не существуют"
            )

        order = Order(
            customer_name=order_data.customer_name,
            status="в обработке"
        )
        self.session.add(order)
        await self.session.flush()  # Получаем order.id для создания связей

        for item in order_data.dishes:
            order_dish = OrderDish(
                order_id=order.id,
                dish_id=item.dish_id,
                quantity=item.quantity
            )
            self.session.add(order_dish)

        await self.session.commit()
        await self.session.refresh(order)
        logger.info(f"Заказ ID={order.id} успешно создан")
        return order

    async def delete_order(self, order_id: int) -> None:
        """
        Отменить заказ, если он в статусе 'в обработке'.
        """
        logger.info(f"Попытка удалить заказ ID={order_id}")
        order = await self.session.get(Order, order_id)
        if not order:
            logger.error(f"Заказ ID={order_id} не найден")
            raise HTTPException(status_code=404, detail="Заказ не найден")

        if order.status != "в обработке":
            logger.warning(f"Нельзя удалить заказ ID={order_id} в статусе '{order.status}'")
            raise HTTPException(
                status_code=400,
                detail="Заказ можно отменить только в статусе 'в обработке'"
            )

        # Удаляем заказ и связанные записи в OrderDish (cascade должен быть настроен, но лучше явно)
        # При необходимости можно добавить явное удаление связанных order_dish
        await self.session.delete(order)
        await self.session.commit()
        logger.info(f"Заказ ID={order_id} успешно удалён")

    async def update_order_status(self, order_id: int, new_status: str) -> Order:
        """
        Изменить статус заказа, соблюдая разрешённые переходы:
        'в обработке' → 'готовится' → 'доставляется' → 'завершен'
        """
        logger.info(f"Изменение статуса заказа ID={order_id} на '{new_status}'")
        order = await self.session.get(Order, order_id)
        if not order:
            logger.error(f"Заказ ID={order_id} не найден")
            raise HTTPException(status_code=404, detail="Заказ не найден")

        valid_transitions = {
            "в обработке": "готовится",
            "готовится": "доставляется",
            "доставляется": "завершен"
        }

        current = order.status
        if valid_transitions.get(current) != new_status:
            logger.warning(f"Недопустимый переход статуса: '{current}' → '{new_status}'")
            raise HTTPException(
                status_code=400,
                detail=f"Нельзя изменить статус с '{current}' на '{new_status}'"
            )

        order.status = new_status
        await self.session.commit()
        await self.session.refresh(order)
        logger.info(f"Статус заказа ID={order_id} успешно изменён на '{new_status}'")
        return order
