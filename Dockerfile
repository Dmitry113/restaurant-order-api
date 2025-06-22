# Dockerfile
FROM python:3.11-slim

# Логирование без буфера
ENV PYTHONUNBUFFERED=1

# Установка зависимостей системы
RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean

# Установка рабочей директории
WORKDIR /app

# Установка зависимостей Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Запуск FastAPI с автообновлением
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
