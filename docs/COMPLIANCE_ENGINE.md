# Compliance Engine v0.8

## Obiettivo

Il motore esegue una pre-verifica strutturata del fascicolo immobiliare.

## Regole iniziali

- identificazione catastale completa;
- quote proprietarie pari al 100%;
- atto di provenienza presente;
- visura e planimetria presenti;
- APE presente;
- visura ipotecaria presente;
- documenti elaborati senza errori;
- assenza di criticità pregresse aperte.

## Esiti

- `VERIFIED_PLUS`
- `VERIFIED`
- `CONDITIONAL`
- `NOT_VERIFIED`

## Findings

Ogni regola non superata genera una criticità con severità:

- INFO
- LOW
- MEDIUM
- HIGH
- CRITICAL

## Limite giuridico

Il motore non certifica conformità urbanistica, catastale,
ipotecaria o legale in senso professionale o pubblico.
Fornisce un supporto organizzativo e documentale.
