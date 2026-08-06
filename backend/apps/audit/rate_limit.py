from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            not settings.RATE_LIMIT_ENABLED
            or not request.path.startswith("/api/")
            or request.path in {"/api/health/"}
        ):
            return self.get_response(request)

        forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
        client_ip = forwarded.split(",")[0].strip() if forwarded else request.META.get("REMOTE_ADDR", "unknown")
        bucket = f"rate:{client_ip}:{request.path}:{request.method}"
        current = cache.get(bucket)

        if current is None:
            cache.set(bucket, 1, timeout=settings.RATE_LIMIT_WINDOW_SECONDS)
        elif current >= settings.RATE_LIMIT_REQUESTS:
            return JsonResponse(
                {"detail": "Limite richieste superato. Riprovare più tardi."},
                status=429,
            )
        else:
            try:
                cache.incr(bucket)
            except ValueError:
                cache.set(bucket, current + 1, timeout=settings.RATE_LIMIT_WINDOW_SECONDS)

        return self.get_response(request)
