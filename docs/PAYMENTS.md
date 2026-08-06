# Pagamenti v0.7

## Architettura

Il pagamento usa un'interfaccia provider:

- `BasePaymentProvider`
- `MockPaymentProvider`

Il modello consente di aggiungere provider reali senza modificare
il ciclo di vita dell'ordine.

## Idempotenza

La creazione intento supporta l'header:

`Idempotency-Key`

## Webhook

Gli eventi in ingresso sono:

- `payment.succeeded`
- `payment.failed`

La firma viene verificata tramite HMAC SHA-256.
