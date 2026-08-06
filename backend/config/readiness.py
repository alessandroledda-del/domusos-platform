from django.conf import settings
from django.http import JsonResponse
from apps.accounts.models import User
from apps.catalog.models import Service

def readiness_view(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({"detail": "Non autorizzato."}, status=403)

    checks = {
        "debug_disabled": not settings.DEBUG,
        "secret_key_changed": settings.SECRET_KEY not in {"dev-secret-key", "change-me-in-production"},
        "allowed_hosts_configured": bool(settings.ALLOWED_HOSTS),
        "catalog_loaded": Service.objects.filter(is_active=True).exists(),
        "admin_exists": User.objects.filter(is_superuser=True).exists(),
        "email_configured": bool(settings.DEFAULT_FROM_EMAIL),
        "antivirus_enabled": bool(settings.ANTIVIRUS_ENABLED),
        "s3_enabled": bool(settings.USE_S3),
    }

    ready = all(checks.values())
    return JsonResponse({
        "ready": ready,
        "checks": checks,
        "version": "1.0.0-rc1",
    }, status=200 if ready else 503)
