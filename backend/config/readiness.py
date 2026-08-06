from django.conf import settings
from rest_framework import permissions, response, status, views
from apps.accounts.models import User
from apps.catalog.models import Service

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
            "antivirus_enabled": bool(settings.ANTIVIRUS_ENABLED),
            "s3_enabled": bool(settings.USE_S3),
        }
        ready = all(checks.values())
        return response.Response(
            {
                "ready": ready,
                "checks": checks,
                "version": "1.0.1",
            },
            status=status.HTTP_200_OK if ready else status.HTTP_503_SERVICE_UNAVAILABLE,
        )
