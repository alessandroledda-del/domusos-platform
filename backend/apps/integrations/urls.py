from rest_framework.routers import DefaultRouter
from .views import InboundEventViewSet, WebhookDeliveryViewSet, WebhookEndpointViewSet

router = DefaultRouter()
router.register("webhook-endpoints", WebhookEndpointViewSet, basename="webhook-endpoint")
router.register("webhook-deliveries", WebhookDeliveryViewSet, basename="webhook-delivery")
router.register("inbound-events", InboundEventViewSet, basename="inbound-event")
urlpatterns = router.urls
