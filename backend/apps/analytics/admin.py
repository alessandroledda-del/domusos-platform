from django.contrib import admin
from .models import AnalyticsSnapshot

@admin.register(AnalyticsSnapshot)
class AnalyticsSnapshotAdmin(admin.ModelAdmin):
    list_display = ("scope", "scope_id", "period_date", "generated_by", "created_at")
    list_filter = ("scope", "period_date")
