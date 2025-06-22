import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# Загружаем .env из корня проекта
load_dotenv()

# Получаем объект конфигурации Alembic
config = context.config

# Получаем DATABASE_URL из окружения
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in .env")

# Заменяем asyncpg на psycopg2 для синхронного подключения (только для Alembic)
SYNC_DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg", "postgresql+psycopg2")

print(f"Using sync DATABASE_URL for alembic: {SYNC_DATABASE_URL}")

# Устанавливаем URL в конфигурацию Alembic
config.set_main_option("sqlalchemy.url", SYNC_DATABASE_URL)

# Настроить логирование
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Импортируем модели и базу для автогенерации
from app.database import Base
import app.models.models  # Здесь должны быть все модели, задекларированные через Base

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
