import pytest

dish_payload = {
    "name": "Пицца Маргарита",
    "description": "Классическая пицца с томатами и моцареллой",
    "price": 450.0,
    "category": "Основные блюда"
}

@pytest.mark.asyncio
async def test_create_dish(async_client):
    response = await async_client.post("/dishes/", json=dish_payload)
    assert response.status_code == 201
    assert response.json()["name"] == dish_payload["name"]

@pytest.mark.asyncio
async def test_get_dishes(async_client):
    response = await async_client.get("/dishes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_delete_dish(async_client):
    # Сначала создаём блюдо
    create_resp = await async_client.post("/dishes/", json=dish_payload)
    dish_id = create_resp.json()["id"]

    # Затем удаляем
    delete_resp = await async_client.delete(f"/dishes/{dish_id}")
    assert delete_resp.status_code == 204
