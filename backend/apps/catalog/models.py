from decimal import Decimal
from django.db import models

class ServiceCategory(models.Model):
    code = models.SlugField(max_length=50, unique=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name_plural = "Service categories"

    def __str__(self):
        return self.name

class Service(models.Model):
    class DeliveryMode(models.TextChoices):
        AUTOMATIC = "AUTOMATIC", "Automatico"
        MANUAL = "MANUAL", "Manuale"
        HYBRID = "HYBRID", "Ibrido"

    code = models.SlugField(max_length=80, unique=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.PROTECT, related_name="services")
    name = models.CharField(max_length=180)
    short_description = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2, default=22)
    sla_hours = models.PositiveIntegerField(default=24)
    delivery_mode = models.CharField(max_length=20, choices=DeliveryMode.choices, default=DeliveryMode.MANUAL)
    required_fields = models.JSONField(default=list, blank=True)
    required_documents = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["category__sort_order", "sort_order", "name"]

    def __str__(self):
        return self.name

    @property
    def gross_price(self):
        return (self.base_price * (Decimal("1") + self.vat_rate / Decimal("100"))).quantize(Decimal("0.01"))
