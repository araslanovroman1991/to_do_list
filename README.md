### Quick start
```bash
cd $directory
poetry shell
poetry env use $(which python3.11)
poetry install -vvv --no-root
export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring

Add this env
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

Then
sudo docker compose up -d --build
```

### Pre-commit
```bash
[pre-commit](https://pre-commit.com/) is de facto standard now for pre push activities like isort or black.
It will format and notify about minor errors like extra whitespaces when you do git commit to your changes automatically.
```bash

# Install pre-commit
pre-commit install
# Run formatting
pre-commit run --all-files

Автопроверка
ruff check .
Автоформатирование
black .
Сортируем импорты
ruff check . --select I --fix
Удаляем несортируемые импорты
ruff check . --select F401 --fix
```

### Other Comands
```bash
python manage.py createsuperuser
uvicorn app.config.app_factory:application --port 9015 --lifespan on
poetry run data_forge first-migrate
poetry run data_forge insert-data
poetry run data_forge create-super-user
python manage.py runserver 0.0.0.0:8000
```