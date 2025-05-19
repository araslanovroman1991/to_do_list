#!/bin/bash

set -e 
# Выполняем подготовительные команды
poetry run python manage.py makemigrations app
poetry run python manage.py migrate
# echo "First migration completed"
poetry run data_forge insert-data
# echo "First insert data completed"
poetry run data_forge create-super-user
# echo "Super user created"

# Запускаем ASGI-сервер
exec poetry run uvicorn app.config.app_factory:application \
    --host 0.0.0.0 \
    --port "${DB_CRUD_PORT}" \
    --lifespan on