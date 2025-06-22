import pytest
import asyncio
from unittest.mock import AsyncMock

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from app.services.order_service import OrderService
from app.models import Order, Dish, OrderDish
from app.schemas.order import OrderCreate


@pytest.fixture
def fake_session():
    # Мокаем AsyncSession
    session = AsyncMock(spec=AsyncSession)
    return session


@pytest.mark.asyncio
async def test_create_order_success(fake_session):
    # Создаём сервис с мок сессией
    service = OrderService(fake_session)

    # Данные заказа с двумя блюдами
    order_data = OrderCreate(
        customer_name="Иван",
        dishes=[
            {"dish_id": 1, "quantity": 2},
            {"dish_id": 2, "quantity": 1}
        ]
    )

    # Мокаем ответ запроса существующих блюд (2 блюда найдены)
    fake_session.execute.return_value.scalars.return_value.all.return_value = [
        Dish(id=1, name="Пицца", description="", price=500.0, category="Основные"),
        Dish(id=2, name="Салат", description="", price=300.0, category="Закуски")
    ]

    # Мокаем flush, commit и refresh
    fake_session.flush.return_value = asyncio.Future()
    fake_session.flush.return_value.set_result(None)
    fake_session.commit.return_value = asyncio.Future()
    fake_session.commit.return_value.set_result(None)
    fake_session.refresh.return_value = asyncio.Future()
    fake_session.refresh.return_value.set_result(None)

    # Запускаем создание заказа
    order = await service.create_order(order_data)

    # Проверяем, что заказ добавлен в сессию
    fake_session.add.assert_any_call(order)

    # Проверяем статус заказа
    assert order.status == "в обработке"


@pytest.mark.asyncio
async def test_create_order_invalid_dish(fake_session):
    service = OrderService(fake_session)
    order_data = OrderCreate(
        customer_name="Иван",
        dishes=[{"dish_id": 1, "quantity": 1}]
    )

    # Возвращаем пустой список блюд — блюдо не найдено
    fake_session.execute.return_value.scalars.return_value.all.return_value = []

    with pytest.raises(HTTPException) as exc_info:
        await service.create_order(order_data)
    assert exc_info.value.status_code == 400
    assert "не существуют" in exc_info.value.detail


@pytest.mark.asyncio
async def test_delete_order_wrong_status(fake_session):
    service = OrderService(fake_session)

    # Мокаем get для возврата заказа со статусом "готовится"
    order = Order(id=1, customer_name="Иван", status="готовится")
    fake_session.get.return_value = order

    with pytest.raises(HTTPException) as exc_info:
        await service.delete_order(1)
    assert exc_info.value.status_code == 400
    assert "можно отменить только в статусе" in exc_info.value.detail


@pytest.mark.asyncio
async def test_update_order_status_invalid_transition(fake_session):
    service = OrderService(fake_session)

    order = Order(id=1, customer_name="Иван", status="в обработке")
    fake_session.get.return_value = order

    with pytest.raises(HTTPException) as exc_info:
        # Попытка перейти из "в обработке" сразу в "доставляется" — пропущен "готовится"
        await service.update_order_status(1, "доставляется")
    assert exc_info.value.status_code == 400
    assert "Нельзя изменить статус" in exc_info.value.detail
