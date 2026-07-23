from django.db import connections
from django.db.utils import OperationalError
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
def live(request):
    return Response({'status': 'ok', 'timestamp': timezone.now().isoformat()})


@api_view(['GET'])
@permission_classes([AllowAny])
def ready(request):
    database_status = 'ok'
    status_code = 200

    try:
        with connections['default'].cursor() as cursor:
            cursor.execute('SELECT 1')
            cursor.fetchone()
    except OperationalError:
        database_status = 'error'
        status_code = 503

    return Response(
        {
            'status': 'ok' if database_status == 'ok' else 'degraded',
            'checks': {
                'database': database_status,
            },
            'timestamp': timezone.now().isoformat(),
        },
        status=status_code,
    )
