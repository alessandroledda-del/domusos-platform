from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
class Migration(migrations.Migration):
    initial=True
    dependencies=[migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations=[
        migrations.CreateModel(name='WebhookEndpoint', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('name', models.CharField(max_length=120)), ('url', models.URLField()), ('secret', models.CharField(blank=True, max_length=255)),
            ('subscribed_events', models.JSONField(default=list)), ('is_active', models.BooleanField(default=True)), ('created_at', models.DateTimeField(auto_now_add=True)),
            ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='webhook_endpoints', to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.CreateModel(name='WebhookDelivery', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('event_type', models.CharField(max_length=100)), ('event_id', models.CharField(max_length=100)), ('payload', models.JSONField(default=dict)),
            ('status', models.CharField(choices=[('PENDING','In attesa'),('DELIVERED','Consegnato'),('FAILED','Fallito')], default='PENDING', max_length=20)),
            ('attempts', models.PositiveIntegerField(default=0)), ('response_status', models.PositiveIntegerField(blank=True, null=True)), ('response_body', models.TextField(blank=True)),
            ('last_attempt_at', models.DateTimeField(blank=True, null=True)), ('created_at', models.DateTimeField(auto_now_add=True)),
            ('endpoint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deliveries', to='integrations.webhookendpoint')),
        ], options={'ordering':['-created_at'], 'unique_together': {('endpoint','event_id')}}),
        migrations.CreateModel(name='InboundEvent', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('provider', models.CharField(max_length=50)), ('event_id', models.CharField(max_length=150)), ('event_type', models.CharField(max_length=100)),
            ('payload', models.JSONField(default=dict)), ('processed', models.BooleanField(default=False)), ('processing_error', models.TextField(blank=True)), ('received_at', models.DateTimeField(auto_now_add=True)),
        ], options={'unique_together': {('provider','event_id')}}),
    ]
