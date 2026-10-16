from rest_framework import serializers
from apps.catalog.models import Service
from apps.companies.access import accessible_companies
from apps.properties.access import accessible_properties
from .models import Order, OrderItem, OrderStatusEvent
from .services import add_service_to_order

class OrderItemSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source="service.name", read_only=True)
    line_subtotal = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    line_vat = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    line_total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = "__all__"
        read_only_fields = ["unit_price", "vat_rate", "sla_hours"]

class OrderStatusEventSerializer(serializers.ModelSerializer):
    changed_by_email = serializers.EmailField(source="changed_by.email", read_only=True)

    class Meta:
        model = OrderStatusEvent
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_events = OrderStatusEventSerializer(many=True, read_only=True)
    customer_email = serializers.EmailField(source="customer.email", read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = [
            "number",
            "customer",
            "company",
            "property",
            "status",
            "internal_notes",
            "service_data",
            "subtotal",
            "vat_total",
            "total",
            "paid_at",
            "completed_at",
            "sla_due_at",
            "created_at",
            "updated_at",
        ]

class CreateOrderSerializer(serializers.Serializer):
    service_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1,
    )
    company = serializers.IntegerField(required=False, allow_null=True)
    property = serializers.IntegerField(required=False, allow_null=True)
    customer_notes = serializers.CharField(required=False, allow_blank=True)
    service_data = serializers.JSONField(required=False)

    def validate_service_ids(self, value):
        services = Service.objects.filter(id__in=value, is_active=True)
        if services.count() != len(set(value)):
            raise serializers.ValidationError("Uno o più servizi non sono disponibili.")
        return value

    def validate(self, attrs):
        request = self.context["request"]
        company_id = attrs.get("company")
        property_id = attrs.get("property")

        if company_id and not accessible_companies(request.user).filter(id=company_id).exists():
            raise serializers.ValidationError({"company": "Organizzazione non accessibile."})

        if property_id and not accessible_properties(request.user).filter(id=property_id).exists():
            raise serializers.ValidationError({"property": "Immobile non accessibile."})

        if property_id and company_id:
            if not accessible_properties(request.user).filter(
                id=property_id,
                company_id=company_id,
            ).exists():
                raise serializers.ValidationError("Immobile e organizzazione non corrispondono.")

        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        order = Order.objects.create(
            customer=request.user,
            company_id=validated_data.get("company"),
            property_id=validated_data.get("property"),
            customer_notes=validated_data.get("customer_notes", ""),
            service_data=validated_data.get("service_data", {}),
        )
        services = Service.objects.filter(id__in=validated_data["service_ids"])
        for service in services:
            add_service_to_order(order, service)
        return order
