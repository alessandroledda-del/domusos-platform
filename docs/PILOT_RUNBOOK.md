# Pilot Runbook

## Prima del pilot

- [ ] accordi e privacy approvati;
- [ ] categorie di interessati mappate;
- [ ] ruoli e permessi verificati;
- [ ] backup testato;
- [ ] ripristino testato;
- [ ] email verificate;
- [ ] webhook verificati;
- [ ] provider pagamento deciso;
- [ ] catalogo e prezzi approvati;
- [ ] partner verificati;
- [ ] disclaimer pubblicati;
- [ ] supporto clienti organizzato.

## Utenti pilot

Limitare il pilot a:

- amministratori interni;
- poche agenzie selezionate;
- partner verificati;
- immobili autorizzati;
- documenti non eccedenti il necessario.

## Controllo giornaliero

- health;
- worker Celery;
- code Redis;
- spazio database;
- storage S3;
- errori documenti;
- SLA;
- ordini;
- findings critici;
- webhook falliti.

## Fine pilot

Produrre:

- report incidenti;
- report feedback;
- KPI;
- lista bug;
- decisione go/no-go.
