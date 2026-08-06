# Politica migrazioni v1.0.1

Le migrazioni iniziali sono versionate nel repository.

## Modifica di un modello

1. Modificare il modello.
2. Eseguire `make migrations`.
3. Revisionare il file generato.
4. Eseguire `make migration-check`.
5. Eseguire i test.
6. Includere la migrazione nello stesso commit.

## Produzione

L'entrypoint esegue soltanto:

```bash
python manage.py migrate --noinput
```

Non vengono generate migrazioni nel server production.

## Avvertenza

Le migrazioni incluse sono state validate sintatticamente in questa sessione,
ma non sono state applicate a PostgreSQL perché il runtime Docker non era disponibile.
La pipeline CI deve eseguire `migrate`, test e controllo drift prima del deploy.
