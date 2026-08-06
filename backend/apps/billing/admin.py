from django.contrib import admin
from .models import Invoice, Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order", "provider", "amount", "status", "created_at")
    list_filter = ("provider", "status")

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("number", "order", "customer_name", "total", "status", "issued_at")
    list_filter = ("status", "issued_at")
    search_fields = ("number", "order__number", "customer_name")
