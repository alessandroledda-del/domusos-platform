from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import InvoiceViewSet, PaymentViewSet
from .webhooks import PaymentWebhookView

router = DefaultRouter()
router.register("payments", PaymentViewSet, basename="payment")
router.register("invoices", InvoiceViewSet, basename="invoice")

urlpatterns = [
    path("payment-webhook/", PaymentWebhookView.as_view(), name="payment-webhook"),
] + router.urls
