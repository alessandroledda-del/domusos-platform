from django.conf import settings
from django.db import models
from apps.companies.models import Company

class Property(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Bozza"
        ANALYSIS = "ANALYSIS", "In analisi"
        VERIFIED = "VERIFIED", "Verificato"
        ISSUE = "ISSUE", "Criticità"

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="properties")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    municipality = models.CharField(max_length=100)
    province = models.CharField(max_length=2)
    postal_code = models.CharField(max_length=10, blank=True)
    cadastral_sheet = models.CharField(max_length=30, blank=True)
    cadastral_particle = models.CharField(max_length=30, blank=True)
    cadastral_subaltern = models.CharField(max_length=30, blank=True)
    cadastral_category = models.CharField(max_length=30, blank=True)
    domus_score = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Owner(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="owners")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    fiscal_code = models.CharField(max_length=16, blank=True)
    linked_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_property_records",
    )
    ownership_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=100)
