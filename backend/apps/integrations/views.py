from rest_framework import mixins, viewsets
from .models import InboundEvent, WebhookDelivery, WebhookEndpoint
from .serializers import (
    InboundEventSerializer,
    WebhookDeliverySerializer,
    WebhookEndpointSerializer,
)

class WebhookEndpointViewSet(viewsets.ModelViewSet):
    serializer_class = WebhookEndpointSerializer

    def get_queryset(self):
        return WebhookEndpoint.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class WebhookDeliveryViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = WebhookDeliverySerializer

    def get_queryset(self):
        return WebhookDelivery.objects.filter(endpoint__owner=self.request.user)

class InboundEventViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = InboundEventSerializer

    def get_queryset(self):
        if not self.request.user.is_staff:
            return InboundEvent.objects.none()
        return InboundEvent.objects.all()
