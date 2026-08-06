from django.db import connection
from django.http import JsonResponse
from redis import Redis
from django.conf import settings

def health_check(request):
    database_ok = False
    redis_ok = False

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            database_ok = cursor.fetchone()[0] == 1
    except Exception:
        database_ok = False

    try:
        client = Redis.from_url(settings.CELERY_BROKER_URL)
        redis_ok = bool(client.ping())
    except Exception:
        redis_ok = False

    status_code = 200 if database_ok and redis_ok else 503
    return JsonResponse(
        {
            "status": "ok" if status_code == 200 else "degraded",
            "database": database_ok,
            "redis": redis_ok,
            "version": "0.5.0",
        },
        status=status_code,
    )
