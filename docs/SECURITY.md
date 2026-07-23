# Security

## Authentication and authorization

- JWT access tokens expire after 15 minutes
- Refresh tokens rotate and expire after 7 days
- RBAC is enforced through custom DRF permission classes:
  - `IsAdmin`
  - `IsAdminOrManager`
  - `IsAdminOrManagerOrReadOnly`

## Rate limiting

DRF throttling is enabled globally:
- Anonymous clients: `30/minute`
- Authenticated users: `120/minute`

## Monitoring and logging

- Request logging middleware records method, path, status, duration, user id, and source IP
- Structured logging is configured with `structlog`

## Operational checks

- `/health/` provides liveness
- `/health/ready/` validates database connectivity
- `security.yml` runs dependency review and CodeQL scans

## Dependency controls

Backend and frontend dependencies should be kept aligned with repository manifests and scanned in CI before release.
