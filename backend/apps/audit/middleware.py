from .models import AuditLog

MUTATING_METHODS = {"POST", "PUT", "PATCH", "DELETE"}

class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        user = getattr(request, "user", None)

        if (
            request.method in MUTATING_METHODS
            and request.path.startswith("/api/")
            and user is not None
            and user.is_authenticated
        ):
            AuditLog.objects.create(
                user=user,
                action=f"HTTP_{request.method}",
                entity_type="APIRequest",
                entity_id=request.path[:100],
                metadata={
                    "method": request.method,
                    "path": request.path,
                    "status_code": response.status_code,
                    "remote_addr": request.META.get("REMOTE_ADDR"),
                    "user_agent": request.META.get("HTTP_USER_AGENT", "")[:250],
                    "request_id": getattr(request, "request_id", ""),
                },
            )

        return response
