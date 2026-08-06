from decimal import Decimal
from django.db.models import Avg, Count, Sum
from django.utils import timezone
from apps.billing.models import Invoice, Payment
from apps.compliance.models import Finding, VerificationCertificate, VerificationRun
from apps.documents.models import Document
from apps.orders.models import Order
from apps.properties.models import Property
from apps.workflows.models import Case
from .models import AnalyticsSnapshot

def safe_decimal(value):
    return value if value is not None else Decimal("0.00")

def build_global_metrics():
    orders = Order.objects.all()
    payments = Payment.objects.all()
    invoices = Invoice.objects.all()
    properties = Property.objects.all()
    documents = Document.objects.all()
    cases = Case.objects.all()
    findings = Finding.objects.all()
    verifications = VerificationRun.objects.all()

    order_agg = orders.aggregate(
        order_count=Count("id"),
        gross_order_value=Sum("total"),
        average_order_value=Avg("total"),
    )

    payment_agg = payments.filter(status=Payment.Status.SUCCEEDED).aggregate(
        collected=Sum("amount"),
        payment_count=Count("id"),
    )

    invoice_agg = invoices.filter(status=Invoice.Status.ISSUED).aggregate(
        invoiced=Sum("total"),
        invoice_count=Count("id"),
    )

    return {
        "orders": {
            "total": order_agg["order_count"] or 0,
            "gross_order_value": str(safe_decimal(order_agg["gross_order_value"])),
            "average_order_value": str(safe_decimal(order_agg["average_order_value"])),
            "awaiting_payment": orders.filter(status=Order.Status.AWAITING_PAYMENT).count(),
            "in_progress": orders.filter(status=Order.Status.IN_PROGRESS).count(),
            "completed": orders.filter(status=Order.Status.COMPLETED).count(),
        },
        "payments": {
            "succeeded": payment_agg["payment_count"] or 0,
            "collected": str(safe_decimal(payment_agg["collected"])),
            "failed": payments.filter(status=Payment.Status.FAILED).count(),
        },
        "invoices": {
            "issued": invoice_agg["invoice_count"] or 0,
            "invoiced": str(safe_decimal(invoice_agg["invoiced"])),
        },
        "operations": {
            "properties": properties.count(),
            "verified_properties": properties.filter(status="VERIFIED").count(),
            "documents": documents.count(),
            "documents_failed": documents.filter(status="FAILED").count(),
            "open_cases": cases.exclude(status__in=["COMPLETED", "CANCELLED"]).count(),
        },
        "compliance": {
            "verification_runs": verifications.count(),
            "certificates": VerificationCertificate.objects.filter(status="VALID").count(),
            "open_findings": findings.filter(status__in=["OPEN", "ACKNOWLEDGED"]).count(),
            "critical_findings": findings.filter(
                status__in=["OPEN", "ACKNOWLEDGED"],
                severity="CRITICAL",
            ).count(),
        },
    }

def create_global_snapshot(user=None, period_date=None):
    period_date = period_date or timezone.localdate()
    metrics = build_global_metrics()
    snapshot, _ = AnalyticsSnapshot.objects.update_or_create(
        scope="GLOBAL",
        scope_id="",
        period_date=period_date,
        defaults={
            "metrics": metrics,
            "generated_by": user,
        },
    )
    return snapshot
