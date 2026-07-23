# Architecture

## Overview

DOMUSOS is split into two applications:

- **Backend**: Django 4.2 and Django REST Framework, exposing a JSON API.
- **Frontend**: Next.js 14 App Router application using React, TypeScript, and Tailwind CSS.

PostgreSQL is the primary database. Redis and Celery are planned for cache and background tasks.

```text
Browser
  |
  | HTTP / JSON + JWT
  v
Next.js frontend (:3000)
  |
  v
Django REST API (:8000/api/)
  |
  v
PostgreSQL
```

## Backend

- `core/urls.py` registers JWT token endpoints and includes the API routes.
- `backend/urls.py` registers `UserViewSet`, `CompanyViewSet`, and `PropertyViewSet` with a DRF router.
- `backend/models.py` defines the custom email-based user model plus companies and properties.
- `backend/serializers.py` controls API representations and validation.
- `backend/views.py` implements CRUD and domain actions.

All API viewsets require authentication. JWT authentication is the normal client authentication mechanism.

## Frontend

The frontend uses the App Router. Pages cover login, dashboard, users, companies, and properties. `frontend/lib/api-client.ts` centralizes Axios requests and JWT handling.

## Request flow

1. A user obtains an access and refresh token from `/api/token/`.
2. The frontend sends the access token in the `Authorization` header using the `Bearer` scheme.
3. Django authenticates the request and dispatches it to the relevant viewset.
4. DRF serializes the response as JSON.
