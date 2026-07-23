# Testing

## Backend tests

Install backend dependencies, then run from the repository root:

```bash
python manage.py test backend.tests
```

The backend test suite uses Django's test runner and isolates test data from the development database.

## Frontend checks

Run these commands from `frontend/`:

```bash
npm run type-check
npm run lint
npm run build
```

Run checks before opening a pull request. Tests should cover endpoint behavior, serializer validation, authentication, and frontend API interactions when those areas change.
