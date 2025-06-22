import logging

# Создаём логгер
logger = logging.getLogger("restaurant")
logger.setLevel(logging.INFO)

# Создаём консольный обработчик
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Формат вывода
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
console_handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(console_handler)
