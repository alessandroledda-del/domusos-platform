# Changelog

## v1.0.2

- hardening RBAC e permessi object-level;
- clienti proprietari resi read-only sugli immobili;
- protezione upload, versioning e rielaborazione documenti;
- validazione FK cross-tenant su pratiche e attività;
- stato ordine e relazioni rese server-managed;
- stato PAID riservato al modulo pagamenti;
- pagamento mock bloccato fuori dallo sviluppo per utenti non staff;
- idempotenza pagamenti scoped;
- webhook pagamento vincolato al provider;
- numerazione ordine, fattura e payout resa concorrente-safe;
- gestione compliance limitata ai responsabili autorizzati;
- readiness con verifica reale di storage e antivirus;
- build Next.js production con NEXT_PUBLIC_API_URL a build time;
- CI SQLite + PostgreSQL e test di regressione di sicurezza.

## v1.0.1

- incluse migrazioni iniziali versionate;
- rimosso makemigrations dall'entrypoint;
- aggiunto controllo migration drift;
- aggiornata configurazione test;
- migliorata la validazione della release;
- documentata la procedura di evoluzione dello schema.

## v1.0.0

- release consolidata della piattaforma DomusOS.
