from django.contrib import admin
from .models import Commission, PartnerAssignment, PartnerProfile, PartnerService, Payout

@admin.register(PartnerProfile)
class PartnerProfileAdmin(admin.ModelAdmin):
    list_display = (
        "display_name",
        "professional_type",
        "status",
        "rating",
        "completed_assignments",
        "sla_compliance_rate",
        "is_featured",
    )
    list_filter = ("status", "professional_type", "is_featured")
    search_fields = ("display_name", "legal_name", "vat_number")

@admin.register(PartnerAssignment)
class PartnerAssignmentAdmin(admin.ModelAdmin):
    list_display = ("case", "partner", "status", "agreed_amount", "due_at", "created_at")
    list_filter = ("status", "created_at")

@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = (
        "assignment",
        "gross_amount",
        "platform_amount",
        "partner_amount",
        "status",
        "earned_at",
    )
    list_filter = ("status",)

@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    list_display = ("number", "partner", "amount", "status", "period_start", "period_end")
    list_filter = ("status", "period_start", "period_end")

admin.site.register(PartnerService)
