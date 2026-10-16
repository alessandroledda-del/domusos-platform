import uuid
from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone
from apps.catalog.models import Service
from apps.companies.models import Company
from apps.properties.models import Property

class Order(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Bozza"
        AWAITING_PAYMENT = "AWAITING_PAYMENT", "In attesa di pagamento"
        PAID = "PAID", "Pagato"
        IN_PROGRESS = "IN_PROGRESS", "In lavorazione"
        WAITING_CUSTOMER = "WAITING_CUSTOMER", "In attesa del cliente"
        COMPLETED = "COMPLETED", "Completato"
        CANCELLED = "CANCELLED", "Annullato"
        REFUNDED = "REFUNDED", "Rimborsato"

    number = models.CharField(max_length=30, unique=True, blank=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders")
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="orders", null=True, blank=True)
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, related_name="orders", null=True, blank=True)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.DRAFT)
    customer_notes = models.TextField(blank=True)
    internal_notes = models.TextField(blank=True)
    service_data = models.JSONField(default=dict, blank=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vat_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sla_due_at = models.DateTimeField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.number or f"Ordine {self.pk}"

    def save(self, *args, **kwargs):
        needs_number = not self.number
        if needs_number:
            self.number = f"TMP-{uuid.uuid4().hex[:20]}"
        super().save(*args, **kwargs)
        if needs_number and self.number.startswith("TMP-"):
            number = f"DOM-{timezone.now().year}-{self.pk:06d}"
            type(self).objects.filter(pk=self.pk).update(number=number)
            self.number = number

    def recalculate_totals(self):
        subtotal = sum((item.line_subtotal for item in self.items.all()), Decimal("0.00"))
        vat_total = sum((item.line_vat for item in self.items.all()), Decimal("0.00"))
        self.subtotal = subtotal
        self.vat_total = vat_total
        self.total = subtotal + vat_total
        self.save(update_fields=["subtotal", "vat_total", "total", "updated_at"])

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2)
    sla_hours = models.PositiveIntegerField(default=24)
    delivery_notes = models.TextField(blank=True)

    @property
    def line_subtotal(self):
        return (self.unit_price * self.quantity).quantize(Decimal("0.01"))

    @property
    def line_vat(self):
        return (self.line_subtotal * self.vat_rate / Decimal("100")).quantize(Decimal("0.01"))

    @property
    def line_total(self):
        return self.line_subtotal + self.line_vat

class OrderStatusEvent(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="status_events")
    previous_status = models.CharField(max_length=30, blank=True)
    new_status = models.CharField(max_length=30)
    note = models.TextField(blank=True)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
