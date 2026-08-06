from django.contrib import admin
from .models import InboundEvent, WebhookDelivery, WebhookEndpoint

admin.site.register(WebhookEndpoint)
admin.site.register(WebhookDelivery)
admin.site.register(InboundEvent)
