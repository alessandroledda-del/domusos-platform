#!/usr/bin/env sh
set -eu

TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR="${BACKUP_DIR:-./backups/$TIMESTAMP}"
mkdir -p "$BACKUP_DIR"

echo "Backup PostgreSQL..."
docker compose -f docker-compose.production.yml exec -T db   pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB"   > "$BACKUP_DIR/postgres.sql"

echo "Copia configurazioni..."
cp .env.production "$BACKUP_DIR/env.production.backup"
cp VERSION "$BACKUP_DIR/VERSION"

echo "Il bucket S3 deve essere copiato con lo strumento del provider."
echo "Backup creato in $BACKUP_DIR"
