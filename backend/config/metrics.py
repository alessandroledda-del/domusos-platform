from rest_framework import permissions, response, views
from apps.accounts.models import User
from apps.documents.models import Document
from apps.orders.models import Order
from apps.properties.models import Property
from apps.workflows.models import Case

class MetricsView(views.APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        return response.Response({
            "users_total": User.objects.count(),
            "properties_total": Property.objects.count(),
            "documents_total": Document.objects.count(),
            "orders_total": Order.objects.count(),
            "orders_in_progress": Order.objects.filter(
                status=Order.Status.IN_PROGRESS
            ).count(),
            "cases_open": Case.objects.exclude(
                status__in=["COMPLETED", "CANCELLED"]
            ).count(),
            "version": "1.0.1",
        })
