# Development Setup

## Prerequisites

- Python 3.11 or newer
- Node.js 18 or newer
- PostgreSQL 15 or newer
- Redis (optional; useful for future Celery work)

## Backend

From the repository root:

```bash
python -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
cp backend/.env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The API runs at `http://localhost:8000/api/` and Django Admin at `http://localhost:8000/admin/`.

Configure `.env` with a real `SECRET_KEY` and database credentials. The default development database is PostgreSQL:

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Django signing key |
| `DEBUG` | Enable development mode |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD` | PostgreSQL connection |
| `DB_HOST`, `DB_PORT` | PostgreSQL host and port |
| `CORS_ALLOWED_ORIGINS` | Comma-separated frontend origins |

## Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

The frontend runs at `http://localhost:3000`. Set `NEXT_PUBLIC_API_URL` when the API is not at its default URL.
