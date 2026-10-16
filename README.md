# DOMUSOS Platform v1.0.2

Release di hardening della piattaforma DomusOS, orientata a sicurezza dei tenant, integrità degli ordini e deploy controllato.

## Novità v1.0.2

- RBAC e permessi object-level rafforzati;
- accesso cliente agli immobili in sola lettura;
- protezione documenti e workflow contro modifiche cross-tenant;
- ordini protetti da modifica diretta dello stato e delle relazioni;
- pagamenti con idempotenza scoped e webhook vincolati al provider;
- pagamento mock disabilitato per clienti fuori dallo sviluppo;
- numerazione ordine/fattura/payout basata su PK;
- compliance gestibile solo dai ruoli autorizzati;
- readiness con controlli effettivi su S3 e ClamAV;
- build production Next.js con URL API passato in fase di build;
- CI su SQLite e PostgreSQL;
- test di regressione di sicurezza.

## Avvio sviluppo

    cp .env.example .env
    docker compose up --build

Configurazione iniziale:

    docker compose exec backend python manage.py createsuperuser
    docker compose exec backend python manage.py seed_catalog
    docker compose exec backend python manage.py seed_demo

## Test

SQLite:

    DJANGO_SETTINGS_MODULE=config.settings_test python manage.py test

PostgreSQL:

    DJANGO_SETTINGS_MODULE=config.settings_test_postgres python manage.py test

## Produzione

Usare .env.production.example come base e sostituire tutti i valori placeholder.
La readiness production richiede un provider di pagamento reale: MOCK non è considerato pronto.

## Stato

Adatta a demo avanzate e pilot controllati dopo esito positivo della CI. Prima dell'esposizione pubblica restano necessari revisione legale, DPIA/GDPR, test end-to-end e penetration test.
