import pytest
from datetime import datetime

dish_payload = {
    "name": "Суп Том Ям",
    "description": "Острый суп с креветками",
    "price": 390.0,
    "category": "Супы"
}

@pytest.mark.asyncio
async def test_create_order(async_client):
    # создаём блюдо
    dish = await async_client.post("/dishes/", json=dish_payload)
    dish_id = dish.json()["id"]

    order_payload = {
        "customer_name": "Иван Иванов",
        "dishes": [dish_id]
    }

    response = await async_client.post("/orders/", json=order_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["customer_name"] == "Иван Иванов"
    assert data["status"] == "в обработке"

@pytest.mark.asyncio
async def test_create_order_with_invalid_dish(async_client):
    order_payload = {
        "customer_name": "Петр Петров",
        "dishes": [99999]  # несуществующий id
    }

    response = await async_client.post("/orders/", json=order_payload)
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_update_order_status(async_client):
    # Создаём блюдо и заказ
    dish = await async_client.post("/dishes/", json=dish_payload)
    dish_id = dish.json()["id"]
    order = await async_client.post("/orders/", json={"customer_name": "Ольга", "dishes": [dish_id]})
    order_id = order.json()["id"]

    # Переход в "готовится"
    resp1 = await async_client.patch(f"/orders/{order_id}/status", json={"status": "готовится"})
    assert resp1.status_code == 200
    assert resp1.json()["status"] == "готовится"

    # Переход в "доставляется"
    resp2 = await async_client.patch(f"/orders/{order_id}/status", json={"status": "доставляется"})
    assert resp2.status_code == 200
    assert resp2.json()["status"] == "доставляется"

    # Попытка вернуться назад (ошибка)
    resp3 = await async_client.patch(f"/orders/{order_id}/status", json={"status": "в обработке"})
    assert resp3.status_code == 400

@pytest.mark.asyncio
async def test_cancel_order(async_client):
    # Создаём блюдо и заказ
    dish = await async_client.post("/dishes/", json=dish_payload)
    dish_id = dish.json()["id"]
    order = await async_client.post("/orders/", json={"customer_name": "Алена", "dishes": [dish_id]})
    order_id = order.json()["id"]

    # Удаляем заказ в статусе "в обработке"
    cancel = await async_client.delete(f"/orders/{order_id}")
    assert cancel.status_code == 204
