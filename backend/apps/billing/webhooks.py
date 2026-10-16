from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework import permissions, response, status, views
from apps.integrations.models import InboundEvent
from apps.integrations.signatures import verify_signature
from apps.orders.models import Order
from apps.orders.services import transition_order
from .models import Payment

class PaymentWebhookView(views.APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    @transaction.atomic
    def post(self, request):
        signature = request.headers.get("X-Payment-Signature", "")
        payload = request.data

        if not verify_signature(payload, settings.PAYMENT_WEBHOOK_SECRET, signature):
            return response.Response(
                {"detail": "Firma non valida."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        provider = payload.get("provider", "MOCK")
        event_id = payload.get("event_id")
        event_type = payload.get("event_type")

        if not event_id or not event_type or not payload.get("payment_reference"):
            return response.Response(
                {"detail": "Evento incompleto."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        event, created = InboundEvent.objects.get_or_create(
            provider=provider,
            event_id=event_id,
            defaults={"event_type": event_type, "payload": payload},
        )

        if not created and event.processed:
            return response.Response({"status": "already_processed"})

        try:
            payment = Payment.objects.select_related("order").get(
                provider=provider,
                provider_reference=payload["payment_reference"],
            )
            if event_type == "payment.succeeded":
                payment.status = Payment.Status.SUCCEEDED
                payment.completed_at = timezone.now()
                payment.save(update_fields=["status", "completed_at"])
                if payment.order.status == Order.Status.AWAITING_PAYMENT:
                    transition_order(
                        payment.order,
                        Order.Status.PAID,
                        payment.created_by,
                        "Pagamento confermato tramite webhook.",
                    )
            elif event_type == "payment.failed":
                payment.status = Payment.Status.FAILED
                payment.completed_at = timezone.now()
                payment.save(update_fields=["status", "completed_at"])

            event.processed = True
            event.processing_error = ""
            event.save(update_fields=["processed", "processing_error"])
        except Payment.DoesNotExist:
            event.processing_error = "Pagamento non trovato."
            event.save(update_fields=["processing_error"])
            return response.Response(
                {"detail": "Pagamento non trovato."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return response.Response({"status": "processed"})
