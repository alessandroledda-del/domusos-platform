# Deployment

## Local containers

Use the development stack:

```bash
docker-compose up --build
```

Services:
- PostgreSQL on `5432`
- Redis on `6379`
- Django API on `8000`
- Next.js app on `3000`

## Production containers

Use the production compose file:

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

Set these environment variables before deployment:
- `SECRET_KEY`
- `ALLOWED_HOSTS`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `NEXT_PUBLIC_API_URL`

## CI/CD workflows

- `backend-tests.yml` runs pytest
- `frontend-tests.yml` runs TypeScript checks and Jest
- `lint.yml` runs frontend linting and backend syntax validation
- `security.yml` runs dependency review and CodeQL
- `deploy.yml` builds and publishes backend/frontend images to GHCR

## Reverse proxy

`docker/nginx.conf` proxies:
- `/api/` and `/health/` to Django
- `/` to Next.js
