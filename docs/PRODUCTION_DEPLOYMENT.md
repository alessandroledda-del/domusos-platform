# Deploy production

## Prerequisiti

- server Linux aggiornato;
- Docker e Docker Compose;
- dominio;
- TLS;
- PostgreSQL gestito o volume persistente;
- storage S3;
- SMTP;
- Redis;
- backup esterno;
- monitoraggio;
- secret manager.

## Procedura

1. Copiare `.env.production.example` in `.env.production`.
2. Sostituire tutti i segreti.
3. Configurare domini e TLS.
4. Verificare storage S3.
5. Eseguire:

```bash
docker compose -f docker-compose.production.yml up -d --build
```

6. Applicare migrazioni.
7. Creare superuser.
8. Caricare catalogo.
9. Verificare `/api/health/`.
10. Verificare `/api/readiness/`.
11. Eseguire lo smoke test.
12. Attivare backup.

## Blocco deploy

Non pubblicare se readiness restituisce `ready: false`.
