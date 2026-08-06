#!/usr/bin/env sh
set -eu

BASE_URL="${BASE_URL:-http://localhost:8000}"

echo "Health..."
curl -fsS "$BASE_URL/api/health/" >/dev/null

echo "Schema OpenAPI..."
curl -fsS "$BASE_URL/api/schema/" >/dev/null

echo "Frontend..."
curl -fsS "${FRONTEND_URL:-http://localhost:3000}" >/dev/null

echo "Smoke test completato."
