from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework import permissions, response, status, views
from apps.accounts.models import User
from apps.catalog.models import Service

def _check_storage():
    if not settings.USE_S3:
        return False
    try:
        default_storage.exists("__domusos_readiness_probe__")
        return True
    except Exception:
        return False

def _check_antivirus():
    if not settings.ANTIVIRUS_ENABLED:
        return False
    try:
        import pyclamd
        client = pyclamd.ClamdNetworkSocket(
            host=settings.CLAMAV_HOST,
            port=settings.CLAMAV_PORT,
            timeout=3,
        )
        return bool(client.ping())
    except Exception:
        return False

class ReadinessView(views.APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        checks = {
            "debug_disabled": not settings.DEBUG,
            "secret_key_changed": settings.SECRET_KEY not in {
                "dev-secret-key",
                "change-me-in-production",
            },
            "allowed_hosts_configured": bool(settings.ALLOWED_HOSTS),
            "catalog_loaded": Service.objects.filter(is_active=True).exists(),
            "admin_exists": User.objects.filter(is_superuser=True).exists(),
            "email_configured": bool(settings.DEFAULT_FROM_EMAIL),
            "antivirus_reachable": _check_antivirus(),
            "storage_reachable": _check_storage(),
        }
        ready = all(checks.values())
        return response.Response(
            {"ready": ready, "checks": checks, "version": "1.0.2"},
            status=status.HTTP_200_OK if ready else status.HTTP_503_SERVICE_UNAVAILABLE,
        )
