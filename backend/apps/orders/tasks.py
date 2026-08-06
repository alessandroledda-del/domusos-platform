from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from apps.notifications.models import Notification
from .models import Order

@shared_task
def check_sla_risk_task():
    now = timezone.now()
    warning_limit = now + timedelta(hours=6)

    risky_orders = Order.objects.filter(
        status__in=[Order.Status.PAID, Order.Status.IN_PROGRESS],
        sla_due_at__isnull=False,
        sla_due_at__lte=warning_limit,
    )

    notified = 0
    for order in risky_orders:
        Notification.objects.get_or_create(
            user=order.customer,
            title=f"SLA in scadenza: {order.number}",
            message="L'ordine è vicino alla scadenza prevista.",
            level=Notification.Level.WARNING,
        )
        notified += 1

    return notified
