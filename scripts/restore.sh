#!/usr/bin/env sh
set -eu

if [ "$#" -ne 1 ]; then
  echo "Uso: scripts/restore.sh <cartella-backup>"
  exit 1
fi

BACKUP_DIR="$1"

if [ ! -f "$BACKUP_DIR/postgres.sql" ]; then
  echo "File postgres.sql non trovato."
  exit 1
fi

echo "Ripristino PostgreSQL..."
cat "$BACKUP_DIR/postgres.sql" |   docker compose -f docker-compose.production.yml exec -T db   psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"

echo "Ripristino completato. Verificare separatamente il bucket S3."
