from django.conf import settings
from django.db import models

class Company(models.Model):
    class Type(models.TextChoices):
        AGENCY = "AGENCY", "Agenzia immobiliare"
        TECHNICAL = "TECHNICAL", "Studio tecnico"
        ENTERPRISE = "ENTERPRISE", "Enterprise"
        PARTNER = "PARTNER", "Partner"

    name = models.CharField(max_length=255)
    vat_number = models.CharField(max_length=20, unique=True)
    company_type = models.CharField(max_length=20, choices=Type.choices)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="owned_companies")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CompanyMembership(models.Model):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Amministratore"
        MANAGER = "MANAGER", "Responsabile"
        OPERATOR = "OPERATOR", "Operatore"
        VIEWER = "VIEWER", "Solo lettura"

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="company_memberships")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.OPERATOR)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("company", "user")

    def __str__(self):
        return f"{self.company} - {self.user}"

class CompanyInvitation(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "In attesa"
        ACCEPTED = "ACCEPTED", "Accettato"
        REVOKED = "REVOKED", "Revocato"

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="invitations")
    email = models.EmailField()
    role = models.CharField(max_length=20, choices=CompanyMembership.Role.choices, default=CompanyMembership.Role.OPERATOR)
    token = models.CharField(max_length=64, unique=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="sent_company_invitations")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("company", "email", "status")
