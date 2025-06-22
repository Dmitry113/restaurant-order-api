# 🍽️ FastAPI REST API — Сервис заказов еды

## 📦 Описание

Это REST API-сервис ресторана, реализованный на **FastAPI**, с использованием **PostgreSQL**, **Alembic**, **Docker** и **Docker Compose**.

Функционал:
- Управление блюдами: создание, просмотр, удаление
- Создание заказов с несколькими блюдами и их количеством
- Изменение статуса заказа (в порядке: `pending` → `preparing` → `delivering` → `completed`)
- Отмена заказа
- Swagger-документация

---

## 🚀 Быстрый старт

### 1. Клонировать репозиторий

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo

2. Создать .env файл

Пример содержимого:

POSTGRES_DB=restaurant_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/restaurant_db

Для тестирования добавьте .env.test с аналогичными переменными, изменив имя базы данных.

3. Собрать и запустить проект

docker-compose up --build

4. Swagger-документация
Открой в браузере:
http://localhost:8000/docs

⚙️ Команды
🧪 Запуск тестов

docker-compose exec web pytest

🔄 Применить миграции Alembic

docker-compose exec web alembic upgrade head

🧱 Стек технологий
Python 3.13+

FastAPI

PostgreSQL

SQLAlchemy 2.0 (async)

Alembic

Pydantic

Pytest

Docker & Docker Compose

🧪 Пример API-запросов
POST /dishes/ — создать блюдо

GET /dishes/ — список блюд

POST /orders/ — создать заказ с блюдами

PATCH /orders/{order_id}/status — изменить статус заказа

DELETE /orders/{order_id} — отменить заказ

📂 Структура проекта

.
├── app/
│   ├── models/
│   ├── schemas/
│   ├── routes/
│   ├── database.py
│   ├── main.py
│   └── ...
├── tests/
├── alembic/
├── docker-compose.yml
├── Dockerfile
├── .env
├── .env.test
├── README.md
└── requirements.txt


