from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRoute

from app.database import create_db_and_tables
from app.routers import dishes, orders  # подключаем оба роутера
from pathlib import Path

app = FastAPI(
    title="Restaurant Order API",
    description="API для управления блюдами и заказами в ресторане",
    version="1.0.0",
    swagger_ui_parameters={"lang": "ru"}  # Включаем русский язык для Swagger UI
)

# Указываем путь к шаблонам
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Стартовая HTML-страница
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Инициализация базы данных при старте
@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

# Подключение маршрутов
app.include_router(dishes.router, prefix="/dishes", tags=["Блюда"])
app.include_router(orders.router, prefix="/orders", tags=["Заказы"])
