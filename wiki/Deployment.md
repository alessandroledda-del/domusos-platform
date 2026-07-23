# Deployment

## Production checklist

1. Set `DEBUG=False`.
2. Provide strong, unique `SECRET_KEY` and database credentials through the environment.
3. Set `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS` to production domains.
4. Run database migrations.
5. Collect static files:

   ```bash
   python manage.py collectstatic
   ```

6. Serve Django with Gunicorn:

   ```bash
   gunicorn core.wsgi:application
   ```

7. Build and serve the frontend:

   ```bash
   cd frontend
   npm run build
   npm run start
   ```

8. Put a TLS-terminating reverse proxy such as nginx in front of both services.

When `DEBUG=False`, Django enables HTTPS redirects and secure session/CSRF cookies. Verify proxy headers and health checks in the target hosting environment.
