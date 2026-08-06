from django.contrib import admin
from .models import Finding, VerificationCertificate, VerificationRun

@admin.register(VerificationRun)
class VerificationRunAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "property",
        "status",
        "score",
        "passed_rules",
        "warning_rules",
        "failed_rules",
        "started_at",
    )
    list_filter = ("status", "engine_version")
    search_fields = ("property__title",)

@admin.register(Finding)
class FindingAdmin(admin.ModelAdmin):
    list_display = ("title", "property", "severity", "status", "rule_code", "created_at")
    list_filter = ("severity", "status", "rule_code")
    search_fields = ("title", "description", "property__title")

@admin.register(VerificationCertificate)
class VerificationCertificateAdmin(admin.ModelAdmin):
    list_display = (
        "public_code",
        "property",
        "verified_level",
        "score",
        "status",
        "issued_at",
        "expires_at",
    )
    list_filter = ("status", "verified_level")
    search_fields = ("public_code", "property__title")
