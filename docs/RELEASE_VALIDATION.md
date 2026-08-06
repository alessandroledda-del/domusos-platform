# Validazione release v1.0.0

Controlli eseguiti durante la generazione del pacchetto:

- parsing sintattico di tutti i file Python;
- validazione JSON di `package.json` e `tsconfig.json`;
- controllo dei file essenziali;
- controllo assenza di `.env` e `.env.production`;
- controllo struttura backend/frontend;
- controllo presenza configurazione test e production.

Non eseguiti in questa sessione:

- installazione completa delle dipendenze;
- `django check`;
- test Django reali;
- build Next.js;
- avvio Docker;
- test end-to-end;
- scansione antivirus reale;
- upload MinIO reale.
