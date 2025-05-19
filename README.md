## Internal process in ACPR
## Quickstart

### 1. Install dependencies without docker
```bash
### 1. CD to root
cd $directory

poetry shell
poetry env use $(which python3.11)
poetry install -vvv --no-root
export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring

Запускаем команду 
sudo docker compose up -d --build postgres pgadmin pg_backup
Собираем три сервиса (БД, админка, бэкапер)
Все это с локальным конфигом
POSTGRES_USER="ta_postgres"
POSTGRES_PASSWORD="qwerty"
POSTGRES_DB="to_do_list"
POSTGRES_PORT="9070"
PGADMIN_EMAIL="admin@localhost.com"
PGADMIN_PORT="9071"
DJANGO_ADMIN_PORT="9072"
DB_CRUD_PORT="9073"
DB_SCHEMA="to_do_data"
POSTGRES_HOST="localhost"
POSTGRES_PORT_LOCAL="9070"
DJANGO_SECRET_KEY="dev-secret-key-abc123"

Затем меняем конфиг на докерный (отличается двумя строками,
POSTGRES_PORT_LOCAL и POSTGRES_HOST)
POSTGRES_USER="ta_postgres"
POSTGRES_PASSWORD="qwerty"
POSTGRES_DB="to_do_list"
POSTGRES_PORT="9070"
PGADMIN_EMAIL="admin@localhost.com"
PGADMIN_PORT="9071"
DJANGO_ADMIN_PORT="9072"
DB_CRUD_PORT="9073"
DB_SCHEMA="to_do_data"
POSTGRES_HOST="postgres"
POSTGRES_PORT_LOCAL="5432"
DJANGO_SECRET_KEY="dev-secret-key-abc123"

Проверили, чтобы применился в виртуальной среде poetry
Применяем команды

poetry run python manage.py makemigrations app - создаем миграцию
poetry run python manage.py migrate app - раскатываем миграцию
poetry run data_forge insert-data - раскатываем данные
poetry run data_forge create-super-user - создаем супер юзера

Запускаем админку и crud
sudo docker compose up -d --build django_admin crud
Сори за долгую загрузку, был трабл с typer, пришлось пожертововать 
multistaging, но по итогу typer плохо дружит с cli django

Проверяем админку, admin/admin


### 5. Activate pre-commit
[pre-commit](https://pre-commit.com/) is de facto standard now for pre push activities like isort or black.
It will format and notify about minor errors like extra whitespaces when you do git commit to your changes automatically.
```bash

# Install pre-commit
pre-commit install
# Run formatting
pre-commit run --all-files

python manage.py createsuperuser
uvicorn app.config.app_factory:application --port 9015 --lifespan on
poetry run data_forge first-migrate
poetry run data_forge insert-data
poetry run data_forge create-super-user
python manage.py runserver 0.0.0.0:8000
```