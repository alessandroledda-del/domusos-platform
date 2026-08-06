# DOMUSOS MVP Release Candidate v1.0

Prima release candidate del monorepo DomusOS, predisposta per un pilot commerciale controllato.

## Moduli inclusi

- autenticazione JWT;
- organizzazioni, membri e ruoli;
- immobili, proprietari e dati catastali;
- archivio e versioning documentale;
- MinIO/S3, Redis, Celery e ClamAV;
- OCR PDF e immagini;
- workflow e pratiche;
- catalogo servizi;
- ordini, pagamenti astratti e fatture PDF;
- Domus Verified e motore di conformità;
- portale cliente e portale partner;
- marketplace partner;
- commissioni e payout simulati;
- analytics;
- webhook ed email;
- onboarding guidato;
- dati demo;
- configurazione production;
- backup e ripristino;
- endpoint di stato e metriche;
- checklist per il pilot.

## Avvio sviluppo

```bash
cp .env.example .env
docker compose up --build
```

Configurazione iniziale:

```bash
docker compose exec backend python manage.py createsuperuser
docker compose exec backend python manage.py seed_catalog
docker compose exec backend python manage.py seed_demo
```

## Accessi locali

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Swagger: http://localhost:8000/api/docs/
- Health: http://localhost:8000/api/health/
- Metrics: http://localhost:8000/api/metrics/
- MinIO: http://localhost:9001

## Produzione

È inclusa una configurazione `docker-compose.production.yml` con:

- Nginx;
- Gunicorn;
- servizi senza bind mount del codice;
- health check;
- storage persistente;
- policy di riavvio;
- configurazione TLS predisposta.

Prima del deploy reale leggere:

- `docs/PRODUCTION_DEPLOYMENT.md`
- `docs/PILOT_RUNBOOK.md`
- `docs/SECURITY_HARDENING.md`
- `docs/BACKUP_AND_RESTORE.md`

## Stato

Release Candidate per pilot controllato. Non è una certificazione di conformità normativa,
catastale, urbanistica, ipotecaria o fiscale. Prima di un utilizzo pubblico sono necessarie
revisione legale, DPIA/GDPR, penetration test, provider reali e procedure operative approvate.
