import os
import asyncio
import pytest
from dotenv import load_dotenv
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_async_session
from app.models.models import Base  # все модели тут
from app.database import get_async_session

# Загрузка переменных окружения из .env.test
load_dotenv(".env.test")

# Создание тестового движка
DATABASE_URL = os.getenv("DATABASE_URL")
engine_test = create_async_engine(DATABASE_URL, echo=True, future=True)
TestSessionLocal = async_sessionmaker(engine_test, expire_on_commit=False, class_=AsyncSession)


# Фикстура для создания базы данных
@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine_test.dispose()


# Фикстура сессии
@pytest.fixture()
async def session() -> AsyncSession:
    async with TestSessionLocal() as session:
        yield session


# Переопределение зависимости
@pytest.fixture()
async def async_client(session: AsyncSession):
    async def override_get_async_session():
        yield session

    app.dependency_overrides[get_async_session] = override_get_async_session

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
