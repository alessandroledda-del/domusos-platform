# DOMUSOS Platform v1.0.1

Release di manutenzione della piattaforma DomusOS, orientata alla riproducibilità del database e al deploy controllato.

## Novità v1.0.1

- migrazioni iniziali versionate per tutte le app con modelli;
- produzione senza `makemigrations` automatico;
- controllo CI contro modifiche ai modelli prive di migrazione;
- comando esplicito per generare nuove migrazioni;
- test SQLite eseguiti con le migrazioni reali;
- correzioni ai profili partner e alla validazione degli accessi;
- controlli statici più severi sulla release;
- manifest dei componenti e delle migrazioni.

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

## Migrazioni

Le migrazioni sono incluse nel repository. Dopo una modifica ai modelli:

```bash
make migrations
make migration-check
```

L'avvio production applica esclusivamente migrazioni già versionate.

## Test

```bash
DJANGO_SETTINGS_MODULE=config.settings_test python manage.py test
```

## Stato

Release adatta a demo avanzate e pilot controllati. Rimangono necessari provider reali, revisione legale, DPIA/GDPR, test end-to-end e penetration test prima dell'esposizione pubblica.
