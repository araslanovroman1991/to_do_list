#!/bin/sh
set -e

DATE=$(date +%F)
BACKUP_FILE="/backups/${POSTGRES_DB}_${DATE}.sql"

echo "[BACKUP] Dumping database to $BACKUP_FILE"
PGPASSWORD="$POSTGRES_PASSWORD" pg_dump -h "$POSTGRES_HOST" -U "$POSTGRES_USER" "$POSTGRES_DB" > "$BACKUP_FILE"

echo "[BACKUP] Cleaning up old backups (keeping 3 latest)..."
ls -1t /backups/*.sql | tail -n +4 | xargs -r rm -f

echo "[BACKUP] Done at $(date)"