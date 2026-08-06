# API v0.9

Documentazione interattiva:

- `/api/docs/`
- `/api/schema/`

## Analytics

- GET `/api/analytics/dashboard/`
- POST `/api/analytics/dashboard/snapshot/`
- GET `/api/analytics/dashboard/export_csv/`
- GET `/api/analytics/snapshots/`

## Marketplace

- CRUD `/api/marketplace/partners/`
- GET `/api/marketplace/partners/ranked/`
- CRUD `/api/marketplace/services/`
- CRUD `/api/marketplace/assignments/`
- POST `/api/marketplace/assignments/assign/`
- POST `/api/marketplace/assignments/{id}/accept/`
- POST `/api/marketplace/assignments/{id}/complete/`
- GET `/api/marketplace/commissions/`
- CRUD `/api/marketplace/payouts/`
- POST `/api/marketplace/payouts/generate/`
- POST `/api/marketplace/payouts/{id}/approve/`
- GET `/api/marketplace/dashboard/`
