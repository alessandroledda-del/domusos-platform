# Operations v0.5

## Avvio

```bash
docker compose up --build
```

## Servizi

- `db`: PostgreSQL
- `redis`: broker Celery
- `minio`: object storage
- `minio-init`: creazione bucket
- `backend`: Django API
- `worker`: Celery
- `frontend`: Next.js

## Log worker

```bash
docker compose logs -f worker
```

## Health check

```bash
curl http://localhost:8000/api/health/
```

## Backup minimo

Eseguire backup separati di:

- PostgreSQL;
- bucket S3;
- segreti;
- configurazioni infrastrutturali.
