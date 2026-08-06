from django.contrib import admin
from .models import Service, ServiceCategory

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "sort_order", "is_active")
    list_filter = ("is_active",)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "base_price", "vat_rate", "sla_hours", "is_active")
    list_filter = ("category", "delivery_mode", "is_active", "is_featured")
    search_fields = ("name", "code", "description")
