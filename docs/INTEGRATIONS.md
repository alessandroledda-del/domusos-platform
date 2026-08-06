# Integrazioni v0.7

## Webhook in uscita

Eventi disponibili:

- `order.status_changed`
- `document.processed`
- `invoice.issued`

Ogni richiesta contiene:

- `X-DomusOS-Event`
- `X-DomusOS-Event-ID`
- `X-DomusOS-Signature`

La firma è HMAC SHA-256 sul JSON canonico.

## Webhook pagamento in ingresso

Endpoint:

`POST /api/billing/payment-webhook/`

Header richiesto:

`X-Payment-Signature`

L'elaborazione è idempotente tramite `provider + event_id`.

## Email

Le email sono inviate tramite Celery.

In sviluppo:

`django.core.mail.backends.console.EmailBackend`

In produzione configurare SMTP o provider transazionale.
