# Security & Integrity Fix v1.0.2

## Obiettivo

La v1.0.2 chiude i principali problemi di autorizzazione e integrità individuati nella revisione della v1.0.1.

## Correzioni

- ruoli aziendali applicati alle operazioni di modifica;
- clienti proprietari con accesso in lettura agli immobili;
- upload, modifica e rielaborazione documenti limitati agli utenti autorizzati;
- validazione delle FK di immobili, pratiche e attività;
- partner limitati ai campi operativi consentiti;
- stato ordine non modificabile direttamente dal cliente;
- stato PAID impostabile solo dal modulo pagamenti;
- idempotenza pagamento scoped per provider, ordine e utente;
- webhook pagamento vincolato anche al provider;
- numerazione ordine/fattura/payout basata sulla PK, evitando "ultimo + 1";
- finding e certificati di compliance limitati ai responsabili autorizzati;
- webhook outbound compatibili con SQLite e PostgreSQL;
- readiness con verifica effettiva di storage e antivirus;
- NEXT_PUBLIC_API_URL passato a Next.js durante la build production.

## Nota

Questa release non introduce nuove funzionalità commerciali. È una release di hardening.
