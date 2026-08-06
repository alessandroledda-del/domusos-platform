from rest_framework import serializers
from .models import Invoice, Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = [
            "provider",
            "provider_reference",
            "amount",
            "status",
            "metadata",
            "idempotency_key",
            "created_by",
            "created_at",
            "completed_at",
        ]

class InvoiceSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source="order.number", read_only=True)

    class Meta:
        model = Invoice
        fields = "__all__"
        read_only_fields = [
            "number",
            "status",
            "subtotal",
            "vat_total",
            "total",
            "pdf_file",
            "issued_at",
            "created_at",
        ]
