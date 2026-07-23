from django.conf import settings
from django.db import connections
from django.db.utils import OperationalError
from django.utils import timezone
try:
    from redis import Redis
    from redis.exceptions import RedisError
except ImportError:  # pragma: no cover - redis is installed in production images
    Redis = None

    class RedisError(Exception):
        pass
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
def live(request):
    return Response({'status': 'ok', 'timestamp': timezone.now().isoformat()})


def _database_status():
    try:
        with connections['default'].cursor() as cursor:
            cursor.execute('SELECT 1')
            cursor.fetchone()
        return 'ok'
    except OperationalError:
        return 'error'


def _redis_status():
    redis_url = getattr(settings, 'REDIS_HEALTHCHECK_URL', '')
    if not redis_url:
        return None

    if Redis is None:
        return 'error'

    try:
        Redis.from_url(redis_url).ping()
        return 'ok'
    except (RedisError, ValueError):
        return 'error'


@api_view(['GET'])
@permission_classes([AllowAny])
def ready(request):
    checks = {
        'database': _database_status(),
    }

    redis_status = _redis_status()
    if redis_status is not None:
        checks['redis'] = redis_status

    is_healthy = all(result == 'ok' for result in checks.values())
    return Response(
        {
            'status': 'ok' if is_healthy else 'degraded',
            'checks': checks,
            'timestamp': timezone.now().isoformat(),
        },
        status=200 if is_healthy else 503,
    )
