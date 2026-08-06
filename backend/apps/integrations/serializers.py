from rest_framework import serializers
from .models import InboundEvent, WebhookDelivery, WebhookEndpoint

class WebhookEndpointSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    secret = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = WebhookEndpoint
        fields = "__all__"

class WebhookDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookDelivery
        fields = "__all__"
        read_only_fields = fields

class InboundEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = InboundEvent
        fields = "__all__"
        read_only_fields = fields
