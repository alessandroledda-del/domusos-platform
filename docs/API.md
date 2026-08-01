# API Guide

## OpenAPI Documentation

The backend exposes an OpenAPI schema generated with **drf-spectacular**.

- Schema JSON: `/api/schema/`
- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`

## Authentication

All API endpoints except health checks require JWT authentication.

1. `POST /api/token/` with `email` and `password`
2. Send the `Authorization` header with a valid JWT access token
3. Refresh with `POST /api/token/refresh/`

## RBAC

- `admin`: full API access
- `manager`: write access to users, companies, and properties
- `user` / `guest`: read-only access to companies and properties, self-service user profile access

## Filtering and Pagination

Collection endpoints support paginated responses and filtering.

### Users
- `?ruolo=manager`
- `?stato=active`
- `?email=example`

### Companies
- `?tipo_cliente=enterprise`
- `?ragione_sociale=domus`

### Properties
- `?company_id=1`
- `?status=active`
- `?comune=roma`
- `?provincia=RM`
- `?min_domus_score=70&max_domus_score=95`

Responses use page-based pagination with `count`, `next`, `previous`, and `results`.

## Health Checks

- `GET /health/` — liveness probe
- `GET /health/ready/` — readiness probe with database check
