from io import BytesIO
from django.core.files.base import ContentFile
from django.db import transaction
from django.utils import timezone
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from apps.integrations.tasks import publish_event
from apps.notifications.tasks import send_email_task
from apps.orders.models import Order
from apps.orders.services import transition_order
from .models import Invoice, Payment
from .providers import get_payment_provider

@transaction.atomic
def create_payment_intent(order, user, idempotency_key=None):
    if order.status != Order.Status.AWAITING_PAYMENT:
        raise ValueError("L'ordine non è in attesa di pagamento.")

    if idempotency_key:
        existing = Payment.objects.filter(idempotency_key=idempotency_key).first()
        if existing:
            return existing

    provider = get_payment_provider()
    intent = provider.create_intent(order)

    return Payment.objects.create(
        order=order,
        provider=provider.code,
        provider_reference=intent.reference,
        amount=order.total,
        status=Payment.Status.PENDING,
        metadata={
            "currency": intent.currency,
            "client_secret": intent.client_secret,
            "provider_status": intent.status,
        },
        idempotency_key=idempotency_key,
        created_by=user,
    )

@transaction.atomic
def create_mock_payment(order, user, succeed=True):
    payment = create_payment_intent(order, user)

    if succeed:
        payment.status = Payment.Status.SUCCEEDED
        payment.completed_at = timezone.now()
        payment.save(update_fields=["status", "completed_at"])
        transition_order(order, Order.Status.PAID, user, "Pagamento simulato completato.")
    else:
        payment.status = Payment.Status.FAILED
        payment.completed_at = timezone.now()
        payment.save(update_fields=["status", "completed_at"])

    return payment

def build_invoice_pdf(invoice):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 55
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(45, y, "DOMUSOS - Fattura")
    y -= 28

    pdf.setFont("Helvetica", 10)
    header_lines = [
        f"Numero: {invoice.number}",
        f"Ordine: {invoice.order.number}",
        f"Cliente: {invoice.customer_name}",
        f"Codice fiscale/P.IVA: {invoice.customer_tax_code or '-'}",
        f"Indirizzo: {invoice.customer_address or '-'}",
    ]
    for line in header_lines:
        pdf.drawString(45, y, line[:110])
        y -= 16

    y -= 12
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(45, y, "Descrizione")
    pdf.drawString(330, y, "Imponibile")
    pdf.drawString(430, y, "IVA")
    pdf.drawString(500, y, "Totale")
    y -= 18

    pdf.setFont("Helvetica", 9)
    for item in invoice.order.items.all():
        pdf.drawString(45, y, item.description[:48])
        pdf.drawRightString(395, y, f"EUR {item.line_subtotal}")
        pdf.drawRightString(470, y, f"EUR {item.line_vat}")
        pdf.drawRightString(555, y, f"EUR {item.line_total}")
        y -= 16

    y -= 12
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawRightString(555, y, f"Imponibile: EUR {invoice.subtotal}")
    y -= 16
    pdf.drawRightString(555, y, f"IVA: EUR {invoice.vat_total}")
    y -= 16
    pdf.drawRightString(555, y, f"Totale: EUR {invoice.total}")

    pdf.save()
    buffer.seek(0)
    return buffer.read()

@transaction.atomic
def issue_invoice(order, customer_name, customer_tax_code="", customer_address=""):
    invoice, created = Invoice.objects.get_or_create(
        order=order,
        defaults={
            "customer_name": customer_name,
            "customer_tax_code": customer_tax_code,
            "customer_address": customer_address,
            "subtotal": order.subtotal,
            "vat_total": order.vat_total,
            "total": order.total,
        },
    )
    if not created and invoice.status == Invoice.Status.ISSUED:
        return invoice

    invoice.customer_name = customer_name
    invoice.customer_tax_code = customer_tax_code
    invoice.customer_address = customer_address
    invoice.subtotal = order.subtotal
    invoice.vat_total = order.vat_total
    invoice.total = order.total
    invoice.status = Invoice.Status.ISSUED
    invoice.issued_at = timezone.now()
    invoice.save()

    content = build_invoice_pdf(invoice)
    invoice.pdf_file.save(f"{invoice.number}.pdf", ContentFile(content), save=True)

    publish_event(
        "invoice.issued",
        {
            "invoice_id": invoice.id,
            "invoice_number": invoice.number,
            "order_id": order.id,
            "total": str(invoice.total),
        },
    )
    return invoice
