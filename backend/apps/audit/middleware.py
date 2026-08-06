import json
from .models import AuditLog

MUTATING_METHODS = {"POST", "PUT", "PATCH", "DELETE"}

class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if (
            request.method in MUTATING_METHODS
            and request.path.startswith("/api/")
            and getattr(request, "user", None)
            and request.user.is_authenticated
        ):
            metadata = {
                "method": request.method,
                "path": request.path,
                "status_code": response.status_code,
                "remote_addr": request.META.get("REMOTE_ADDR"),
                "user_agent": request.META.get("HTTP_USER_AGENT", "")[:250],
            }
            AuditLog.objects.create(
                user=request.user,
                action=f"HTTP_{request.method}",
                entity_type="APIRequest",
                entity_id=request.path[:100],
                metadata=metadata,
            )

        return response
