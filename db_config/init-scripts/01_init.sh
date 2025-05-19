#!/bin/bash
set -e

# Получаем переменные окружения
DB_NAME="${POSTGRES_DB}"
DB_USER="${POSTGRES_USER}"

echo "[INIT] Starting database check/init..."
echo "[INIT] Requested DB: $DB_NAME"
echo "[INIT] Owner: $DB_USER"

# Подключаемся к системной базе postgres
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres <<-EOSQL
DO \$\$
BEGIN
   IF NOT EXISTS (
       SELECT FROM pg_database WHERE datname = '$DB_NAME'
   ) THEN
       RAISE NOTICE '[INIT] Creating database "$DB_NAME"...';
       EXECUTE format('CREATE DATABASE "%I" OWNER "%I"', '$DB_NAME', '$DB_USER');
   ELSE
       RAISE NOTICE '[INIT] Database "$DB_NAME" already exists. Skipping.';
   END IF;
END
\$\$;
GRANT ALL PRIVILEGES ON DATABASE "$DB_NAME" TO "$DB_USER";
EOSQL

# 2. Создание схемы внутри базы
echo "[INIT] Connecting to $DB_NAME to create schema $DB_SCHEMA..."

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DB_NAME" <<-EOSQL
DO \$\$
BEGIN
   IF NOT EXISTS (
       SELECT schema_name FROM information_schema.schemata
       WHERE schema_name = '$DB_SCHEMA'
   ) THEN
       RAISE NOTICE '[INIT] Creating schema "$DB_SCHEMA"...';
       EXECUTE format('CREATE SCHEMA "%I" AUTHORIZATION "%I"', '$DB_SCHEMA', '$DB_USER');
   ELSE
       RAISE NOTICE '[INIT] Schema "$DB_SCHEMA" already exists. Skipping.';
   END IF;
END
\$\$;
EOSQL

echo "[INIT] Database and schema initialization complete."