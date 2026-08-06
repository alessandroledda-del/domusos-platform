from django.contrib import admin
from .models import Order, OrderItem, OrderStatusEvent

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("unit_price", "vat_rate", "sla_hours")

class OrderStatusEventInline(admin.TabularInline):
    model = OrderStatusEvent
    extra = 0
    readonly_fields = ("previous_status", "new_status", "changed_by", "created_at")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("number", "customer", "status", "total", "sla_due_at", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("number", "customer__email")
    inlines = [OrderItemInline, OrderStatusEventInline]

admin.site.register(OrderItem)
admin.site.register(OrderStatusEvent)
