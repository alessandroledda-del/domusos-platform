# Domus Verified v0.8

## Requisiti di emissione

Un certificato può essere emesso solo quando l'esito è:

- `VERIFIED`
- `VERIFIED_PLUS`

## Contenuto

- codice pubblico;
- immobile;
- livello;
- punteggio;
- data emissione;
- scadenza;
- snapshot delle regole.

## Verifica pubblica

Endpoint:

`GET /api/compliance/public/{public_code}/`

Pagina frontend:

`/verify/{public_code}`

## Validità

La validità predefinita è 90 giorni.
Il certificato può essere revocato o risultare scaduto.
