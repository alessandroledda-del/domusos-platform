from django.conf import settings
from django.db import models
from apps.orders.models import Order

class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "In attesa"
        SUCCEEDED = "SUCCEEDED", "Completato"
        FAILED = "FAILED", "Fallito"
        REFUNDED = "REFUNDED", "Rimborsato"

    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="payments")
    provider = models.CharField(max_length=40, default="MOCK")
    provider_reference = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    metadata = models.JSONField(default=dict, blank=True)
    idempotency_key = models.CharField(max_length=120, unique=True, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

class Invoice(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Bozza"
        ISSUED = "ISSUED", "Emessa"
        CANCELLED = "CANCELLED", "Annullata"

    order = models.OneToOneField(Order, on_delete=models.PROTECT, related_name="invoice")
    number = models.CharField(max_length=30, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    customer_name = models.CharField(max_length=255)
    customer_tax_code = models.CharField(max_length=30, blank=True)
    customer_address = models.CharField(max_length=255, blank=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    vat_total = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    pdf_file = models.FileField(upload_to="invoices/%Y/%m/", blank=True)
    issued_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.number:
            from django.utils import timezone
            year = timezone.now().year
            prefix = f"INV-{year}-"
            last = Invoice.objects.filter(number__startswith=prefix).order_by("-number").first()
            sequence = int(last.number.split("-")[-1]) + 1 if last else 1
            self.number = f"{prefix}{sequence:06d}"
        super().save(*args, **kwargs)
