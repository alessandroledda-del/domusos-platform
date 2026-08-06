# Limiti noti v1.0.0

## Migrazioni

Il repository conserva i package `migrations` ma, in questa distribuzione,
le migrazioni applicative vengono generate durante il bootstrap del container.

Prima di un deploy pubblico è opportuno:

1. generare le migrazioni in un branch di release;
2. revisionarle;
3. versionarle nel repository;
4. eliminare `makemigrations` dall'entrypoint production.

## Pagamenti

Il provider predefinito è mock. Non vengono acquisiti fondi reali.

## Fatturazione

Il PDF non è fattura elettronica e non viene trasmesso allo SDI.

## OCR

- PDF nativi: estrazione testuale;
- immagini: Tesseract;
- PDF scansionati multipagina: copertura parziale.

## Domus Verified

È una pre-verifica documentale. Non è una certificazione pubblica
o professionale di conformità.

## Payout

Commissioni e payout non effettuano bonifici e non sostituiscono
la contabilità aziendale.

## Frontend

L'interfaccia è funzionale ma ancora essenziale e non include
un design system completo, test browser end-to-end o accessibilità certificata.
