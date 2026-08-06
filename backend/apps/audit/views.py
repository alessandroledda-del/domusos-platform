from rest_framework import mixins, viewsets
from .models import AuditLog
from .serializers import AuditLogSerializer

class AuditLogViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = AuditLogSerializer

    def get_queryset(self):
        return AuditLog.objects.filter(user=self.request.user)
