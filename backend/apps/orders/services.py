from datetime import timedelta
from django.db import transaction
from django.utils import timezone
from apps.integrations.tasks import publish_event
from apps.notifications.models import Notification
from apps.notifications.tasks import send_email_task
from apps.workflows.models import Case, Task
from .models import Order, OrderItem, OrderStatusEvent

ALLOWED_TRANSITIONS = {
    Order.Status.DRAFT: {Order.Status.AWAITING_PAYMENT, Order.Status.CANCELLED},
    Order.Status.AWAITING_PAYMENT: {Order.Status.PAID, Order.Status.CANCELLED},
    Order.Status.PAID: {Order.Status.IN_PROGRESS, Order.Status.REFUNDED},
    Order.Status.IN_PROGRESS: {Order.Status.WAITING_CUSTOMER, Order.Status.COMPLETED, Order.Status.CANCELLED},
    Order.Status.WAITING_CUSTOMER: {Order.Status.IN_PROGRESS, Order.Status.COMPLETED, Order.Status.CANCELLED},
    Order.Status.COMPLETED: set(),
    Order.Status.CANCELLED: set(),
    Order.Status.REFUNDED: set(),
}

def calculate_sla_due(order):
    if not order.items.exists():
        return None
    max_hours = max(item.sla_hours for item in order.items.all())
    start = order.paid_at or timezone.now()
    return start + timedelta(hours=max_hours)

@transaction.atomic
def add_service_to_order(order, service, quantity=1):
    if order.status != Order.Status.DRAFT:
        raise ValueError("È possibile modificare solo ordini in bozza.")

    item = OrderItem.objects.create(
        order=order,
        service=service,
        description=service.name,
        quantity=quantity,
        unit_price=service.base_price,
        vat_rate=service.vat_rate,
        sla_hours=service.sla_hours,
    )
    order.recalculate_totals()
    return item

@transaction.atomic
def transition_order(order, new_status, user=None, note=""):
    if new_status == order.status:
        return order

    allowed = ALLOWED_TRANSITIONS.get(order.status, set())
    if new_status not in allowed:
        raise ValueError(f"Transizione non consentita: {order.status} -> {new_status}")

    previous = order.status
    order.status = new_status

    if new_status == Order.Status.PAID:
        order.paid_at = timezone.now()
        order.sla_due_at = calculate_sla_due(order)
    elif new_status == Order.Status.COMPLETED:
        order.completed_at = timezone.now()

    order.save()

    OrderStatusEvent.objects.create(
        order=order,
        previous_status=previous,
        new_status=new_status,
        note=note,
        changed_by=user,
    )

    Notification.objects.create(
        user=order.customer,
        title=f"Ordine {order.number}",
        message=f"Lo stato dell'ordine è cambiato in: {order.get_status_display()}.",
        level=Notification.Level.INFO,
    )

    send_email_task.delay(
        order.customer.email,
        f"Aggiornamento ordine {order.number}",
        "order_status",
        {
            "order_number": order.number,
            "status_label": order.get_status_display(),
            "total": str(order.total),
        },
    )

    publish_event(
        "order.status_changed",
        {
            "order_id": order.id,
            "order_number": order.number,
            "previous_status": previous,
            "new_status": new_status,
            "total": str(order.total),
        },
    )

    if new_status == Order.Status.PAID and order.property:
        case = Case.objects.create(
            property=order.property,
            title=f"{order.number} - Erogazione servizi",
            service_type=", ".join(item.service.name for item in order.items.all())[:100],
            status=Case.Status.OPEN,
            due_date=order.sla_due_at.date() if order.sla_due_at else None,
            notes=order.customer_notes,
            created_by=user or order.customer,
        )
        for item in order.items.all():
            Task.objects.create(
                case=case,
                title=f"Erogare: {item.service.name}",
                due_date=order.sla_due_at.date() if order.sla_due_at else None,
            )

    return order
