import uuid
import requests
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from .models import WebhookDelivery, WebhookEndpoint
from .signatures import sign_payload

@shared_task(bind=True, autoretry_for=(requests.RequestException,), retry_backoff=True, max_retries=5)
def deliver_webhook_task(self, delivery_id):
    delivery = WebhookDelivery.objects.select_related("endpoint").get(id=delivery_id)
    endpoint = delivery.endpoint
    secret = endpoint.secret or settings.OUTBOUND_WEBHOOK_SECRET
    signature = sign_payload(delivery.payload, secret)

    delivery.attempts += 1
    delivery.last_attempt_at = timezone.now()
    delivery.save(update_fields=["attempts", "last_attempt_at"])

    http_response = requests.post(
        endpoint.url,
        json=delivery.payload,
        headers={
            "X-DomusOS-Event": delivery.event_type,
            "X-DomusOS-Event-ID": delivery.event_id,
            "X-DomusOS-Signature": signature,
        },
        timeout=10,
    )

    delivery.response_status = http_response.status_code
    delivery.response_body = http_response.text[:2000]
    delivery.status = (
        WebhookDelivery.Status.DELIVERED
        if 200 <= http_response.status_code < 300
        else WebhookDelivery.Status.FAILED
    )
    delivery.save(update_fields=["response_status", "response_body", "status"])
    http_response.raise_for_status()
    return delivery.status

def publish_event(event_type, payload):
    event_id = str(uuid.uuid4())
    endpoints = [
        endpoint
        for endpoint in WebhookEndpoint.objects.filter(is_active=True)
        if event_type in (endpoint.subscribed_events or [])
    ]
    deliveries = []
    for endpoint in endpoints:
        delivery = WebhookDelivery.objects.create(
            endpoint=endpoint,
            event_type=event_type,
            event_id=event_id,
            payload=payload,
        )
        deliver_webhook_task.delay(delivery.id)
        deliveries.append(delivery.id)
    return deliveries
