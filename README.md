# domusos-platform

**DOMUSOS** is a PropTech platform for real estate management and intelligent property verification ("Domus Score"). It exposes a Django REST Framework API and a Next.js 14 frontend.

---

## Architecture

```
domusos-platform/
├── manage.py                  # Django CLI entry-point
├── core/                      # Django project package
│   ├── __init__.py
│   ├── urls.py                # Root URL configuration
│   ├── wsgi.py                # WSGI application
│   └── asgi.py                # ASGI application
├── backend/                   # Django application
│   ├── __init__.py
│   ├── apps.py
│   ├── settings.py            # All Django settings
│   ├── models.py              # User, Company, Property
│   ├── serializers.py         # DRF serializers
│   ├── views.py               # DRF ViewSets
│   ├── urls.py                # API router
│   ├── admin.py               # Django admin
│   ├── migrations/            # DB migrations
│   ├── requirements.txt
│   └── .env.example
└── frontend/                  # Next.js 14 App Router
    ├── app/
    │   ├── layout.tsx
    │   ├── page.tsx           # Redirects to /login or /dashboard
    │   ├── login/page.tsx
    │   ├── dashboard/page.tsx
    │   ├── users/
    │   │   ├── page.tsx       # Users list
    │   │   └── [id]/page.tsx  # User detail / edit
    │   ├── companies/
    │   │   ├── page.tsx       # Companies list
    │   │   └── [id]/page.tsx  # Company detail / edit
    │   └── properties/
    │       ├── page.tsx       # Properties list
    │       └── [id]/page.tsx  # Property detail / edit / score update
    ├── lib/
    │   └── api-client.ts      # Axios API client with JWT handling
    ├── package.json
    └── .env.example
```

---

## Tech Stack

| Layer    | Technology                                        |
|----------|---------------------------------------------------|
| Backend  | Python 3.11+, Django 4.2, DRF 3.14, Simple JWT   |
| Database | PostgreSQL 15+                                    |
| Cache/Queue | Redis, Celery                                  |
| Frontend | Next.js 14, React 18, TypeScript, Tailwind CSS   |
| Auth     | JWT (access: 15 min, refresh: 7 days, rotation)  |

---

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis (optional, for Celery tasks)

---

## Backend Setup

### 1. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r backend/requirements.txt
```

### 3. Configure environment variables

```bash
cp backend/.env.example .env
# Edit .env with your real values
```

Key variables:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` for development |
| `DB_NAME / DB_USER / DB_PASSWORD / DB_HOST / DB_PORT` | PostgreSQL connection |
| `JWT_SECRET_KEY` | JWT signing key (defaults to `SECRET_KEY`) |
| `CORS_ALLOWED_ORIGINS` | Comma-separated list of allowed frontend origins |
| `REDIS_HOST / REDIS_PORT` | Redis connection (for Celery) |

### 4. Create the database

```bash
psql -U postgres -c "CREATE DATABASE domusos_db;"
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver
```

API is available at `http://localhost:8000/api/`  
Admin panel at `http://localhost:8000/admin/`

---

## Frontend Setup

### 1. Install dependencies

```bash
cd frontend
npm install
```

### 2. Configure environment variables

```bash
cp .env.example .env.local
# Edit .env.local if your backend runs on a different URL
```

| Variable | Description |
|---|---|
| `NEXT_PUBLIC_API_URL` | Backend API base URL (default: `http://localhost:8000/api`) |

### 3. Start the development server

```bash
npm run dev
```

App is available at `http://localhost:3000`

---

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/token/` | Obtain JWT access + refresh tokens |
| POST | `/api/token/refresh/` | Refresh an access token |

### Users

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/users/` | List all users |
| POST | `/api/users/` | Create a user |
| GET | `/api/users/{id}/` | Get user detail |
| PUT/PATCH | `/api/users/{id}/` | Update a user |
| DELETE | `/api/users/{id}/` | Delete a user |
| GET | `/api/users/me/` | Get current authenticated user |
| POST | `/api/users/{id}/set_password/` | Set a new password |

### Companies

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/companies/` | List all companies |
| POST | `/api/companies/` | Create a company |
| GET | `/api/companies/{id}/` | Get company detail (includes properties) |
| PUT/PATCH | `/api/companies/{id}/` | Update a company |
| DELETE | `/api/companies/{id}/` | Delete a company |
| GET | `/api/companies/{id}/properties/` | List properties for a company |

### Properties

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/properties/` | List all properties (`?company_id=` to filter) |
| POST | `/api/properties/` | Create a property |
| GET | `/api/properties/{id}/` | Get property detail |
| PUT/PATCH | `/api/properties/{id}/` | Update a property |
| DELETE | `/api/properties/{id}/` | Delete a property |
| POST | `/api/properties/{id}/update_score/` | Update Domus Score |
| POST | `/api/properties/{id}/update_status/` | Update status |
| GET | `/api/properties/by_company/?company_id=` | Properties by company |

All endpoints (except `/api/token/`) require a valid JWT ******

```
Authorization: ******
```

---

## Data Models

### User

| Field | Type | Description |
|---|---|---|
| `email` | EmailField (unique) | Login identifier |
| `nome` | CharField | First name |
| `cognome` | CharField | Last name |
| `telefono` | CharField (optional) | Phone number |
| `ruolo` | CharField | `admin` / `user` / `guest` |
| `stato` | CharField | `active` / `inactive` / `suspended` |

### Company

| Field | Type | Description |
|---|---|---|
| `ragione_sociale` | CharField (unique) | Company legal name |
| `partita_iva` | CharField (unique) | VAT number |
| `tipo_cliente` | CharField | `enterprise` / `pme` / `freelance` / `other` |
| `email` | EmailField | Contact email |
| `telefono` | CharField (optional) | Phone |

### Property

| Field | Type | Description |
|---|---|---|
| `company` | ForeignKey → Company | Owner company |
| `indirizzo` | CharField | Street address |
| `comune` | CharField | Municipality |
| `provincia` | CharField (2 chars) | Province code |
| `foglio` | CharField | Land registry sheet |
| `particella` | CharField | Land registry parcel |
| `subalterno` | CharField (optional) | Sub-parcel |
| `categoria_catastale` | CharField | Cadastral category |
| `domus_score` | DecimalField (optional) | Proprietary property score |
| `status` | CharField | `active` / `inactive` / `archived` |

---

## Running Tests

```bash
# Backend
python manage.py test backend

# Frontend type-checking
cd frontend && npm run type-check

# Frontend lint
cd frontend && npm run lint
```

---

## Production Deployment

1. Set `DEBUG=False` in your `.env`
2. Set strong `SECRET_KEY` and `JWT_SECRET_KEY`
3. Run `python manage.py collectstatic`
4. Use **Gunicorn** as the WSGI server: `gunicorn core.wsgi:application`
5. Serve the frontend with `npm run build && npm run start` (or export to a CDN)
6. Place a reverse proxy (e.g. nginx) in front of both services
