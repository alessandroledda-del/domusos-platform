# AI Integration Guide

## Authentication flow for machine clients

1. Obtain tokens with `POST /api/token/` using an email/password pair.
2. Send the access token in the `Authorization` header with the standard HTTP bearer scheme on protected endpoints.
3. When the access token expires, refresh it with `POST /api/token/refresh/`.
4. Replace the stored refresh token after each successful refresh because rotation is enabled.

## Token refresh behavior

- Access tokens live for 15 minutes.
- Refresh tokens live for 7 days.
- Refresh tokens are rotated on every refresh response.
- Failed refresh attempts return the standard error payload described below.

## Standard error format

The API keeps successful payloads unchanged. Error responses are normalized to this shape:

```json
{
  "code": "validation_error",
  "message": "This field is required.",
  "details": {
    "password": ["This field is required."]
  },
  "trace_id": "8d9a1d82-9b63-41d6-8e6f-3c0b635f0f1b"
}
```

### Field meanings

- `code`: stable machine-friendly category or backend error code.
- `message`: short human-readable summary.
- `details`: raw field or framework error details.
- `trace_id`: request correlation identifier for support and retries.

## Trace ID usage

- Every response includes an `X-Trace-Id` header.
- If a client sends `X-Trace-Id`, the backend reuses it.
- Error bodies echo the same `trace_id` value for log correlation.

## Rate-limit expectations

The Django app does not currently enforce endpoint-specific rate limits. Clients should still:

- use exponential backoff for 401/429/5xx retries,
- avoid parallel refresh storms,
- treat infrastructure-level throttling as possible even if the app itself does not emit 429s.

## Readiness and dependency awareness

- `GET /health/` returns liveness status.
- `GET /health/ready/` checks the primary database.
- If `REDIS_URL`, `CELERY_BROKER_URL`, or `CELERY_RESULT_BACKEND` is configured, readiness also checks Redis.
- Readiness returns HTTP 503 with `status: degraded` when a critical dependency fails.

## Minimal integration examples

### Obtain tokens

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@example.com","password":"secret123"}'
```

### Refresh a token

```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H 'Content-Type: application/json' \
  -H 'X-Trace-Id: agent-run-42' \
  -d '{"refresh":"<refresh-token>"}'
```

### Handle machine-friendly errors in Python

```python
import requests

response = requests.post(
    'http://localhost:8000/api/users/999/set_password/',
    headers={
        'Authorization': 'Bearer ' + access_token,
        'X-Trace-Id': 'agent-run-42',
    },
    json={},
)

if response.status_code >= 400:
    payload = response.json()
    print(payload['code'], payload['message'], payload['trace_id'])
```
