from django.http import JsonResponse
from django.db import connection
from apps.accounts.models import User
from apps.documents.models import Document
from apps.orders.models import Order
from apps.properties.models import Property
from apps.workflows.models import Case

def metrics_view(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({"detail": "Non autorizzato."}, status=403)

    return JsonResponse({
        "users_total": User.objects.count(),
        "properties_total": Property.objects.count(),
        "documents_total": Document.objects.count(),
        "orders_total": Order.objects.count(),
        "orders_in_progress": Order.objects.filter(status=Order.Status.IN_PROGRESS).count(),
        "cases_open": Case.objects.exclude(status__in=["COMPLETED", "CANCELLED"]).count(),
        "database_vendor": connection.vendor,
        "version": "1.0.0-rc1",
    })
