# Backup e ripristino

## Oggetti da proteggere

- PostgreSQL;
- bucket S3;
- configurazioni;
- segreti;
- certificati;
- log di audit secondo retention.

## Frequenza suggerita

- database: giornaliero;
- storage: versioning continuo;
- configurazioni: a ogni release;
- test ripristino: mensile.

## Script

Backup:

```bash
scripts/backup.sh
```

Restore:

```bash
scripts/restore.sh backups/<timestamp>
```

Gli script sono una base operativa e devono essere adattati
all'infrastruttura e al provider effettivo.
