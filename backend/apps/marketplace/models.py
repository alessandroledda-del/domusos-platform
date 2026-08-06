from decimal import Decimal
from django.conf import settings
from django.db import models
from apps.catalog.models import Service
from apps.orders.models import Order
from apps.workflows.models import Case

class PartnerProfile(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Bozza"
        PENDING = "PENDING", "In verifica"
        ACTIVE = "ACTIVE", "Attivo"
        SUSPENDED = "SUSPENDED", "Sospeso"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="partner_profile")
    display_name = models.CharField(max_length=255)
    legal_name = models.CharField(max_length=255, blank=True)
    vat_number = models.CharField(max_length=30, blank=True)
    professional_type = models.CharField(max_length=100)
    license_number = models.CharField(max_length=100, blank=True)
    provinces = models.JSONField(default=list)
    remote_service = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    completed_assignments = models.PositiveIntegerField(default=0)
    average_completion_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sla_compliance_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_featured", "-rating", "display_name"]

    def __str__(self):
        return self.display_name

class PartnerService(models.Model):
    partner = models.ForeignKey(PartnerProfile, on_delete=models.CASCADE, related_name="service_offers")
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="partner_offers")
    partner_price = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_hours = models.PositiveIntegerField(default=24)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("partner", "service")

class PartnerAssignment(models.Model):
    class Status(models.TextChoices):
        PROPOSED = "PROPOSED", "Proposta"
        ACCEPTED = "ACCEPTED", "Accettata"
        IN_PROGRESS = "IN_PROGRESS", "In lavorazione"
        COMPLETED = "COMPLETED", "Completata"
        REJECTED = "REJECTED", "Rifiutata"
        CANCELLED = "CANCELLED", "Annullata"

    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="partner_assignments")
    partner = models.ForeignKey(PartnerProfile, on_delete=models.PROTECT, related_name="assignments")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name="partner_assignments")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PROPOSED)
    agreed_amount = models.DecimalField(max_digits=10, decimal_places=2)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=20)
    due_at = models.DateTimeField(null=True, blank=True)
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="created_partner_assignments")
    accepted_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def commission_amount(self):
        return (self.agreed_amount * self.commission_rate / Decimal("100")).quantize(Decimal("0.01"))

    @property
    def partner_net_amount(self):
        return self.agreed_amount - self.commission_amount

class Commission(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "In attesa"
        EARNED = "EARNED", "Maturata"
        PAID = "PAID", "Pagata"
        CANCELLED = "CANCELLED", "Annullata"

    assignment = models.OneToOneField(PartnerAssignment, on_delete=models.PROTECT, related_name="commission")
    gross_amount = models.DecimalField(max_digits=10, decimal_places=2)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2)
    platform_amount = models.DecimalField(max_digits=10, decimal_places=2)
    partner_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    earned_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Payout(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Bozza"
        APPROVED = "APPROVED", "Approvato"
        PAID = "PAID", "Pagato"
        FAILED = "FAILED", "Fallito"

    partner = models.ForeignKey(PartnerProfile, on_delete=models.PROTECT, related_name="payouts")
    number = models.CharField(max_length=30, unique=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    period_start = models.DateField()
    period_end = models.DateField()
    notes = models.TextField(blank=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_partner_payouts",
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.number:
            from django.utils import timezone
            year = timezone.now().year
            prefix = f"PAY-{year}-"
            last = Payout.objects.filter(number__startswith=prefix).order_by("-number").first()
            sequence = int(last.number.split("-")[-1]) + 1 if last else 1
            self.number = f"{prefix}{sequence:06d}"
        super().save(*args, **kwargs)
