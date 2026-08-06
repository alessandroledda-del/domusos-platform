# Architettura DomusOS v0.5

## Componenti

- Next.js: interfaccia web
- Django REST Framework: API
- PostgreSQL: dati strutturati
- Redis: broker e backend task
- Celery: elaborazioni asincrone
- MinIO: object storage S3 compatibile
- Swagger/OpenAPI: documentazione API

## Flusso documentale

1. caricamento documento;
2. salvataggio su MinIO;
3. creazione task Celery;
4. estrazione testuale dai PDF;
5. classificazione;
6. aggiornamento metadati;
7. notifica utente.

## Storage

In sviluppo viene utilizzato MinIO.
In produzione è possibile usare un provider S3 compatibile
modificando esclusivamente le variabili d'ambiente.

## Limiti OCR

La v0.5 estrae testo dai PDF nativi.
I PDF scansionati senza livello testuale richiederanno
un motore OCR immagini nella release successiva.
