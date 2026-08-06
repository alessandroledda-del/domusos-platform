from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
class Migration(migrations.Migration):
    initial=True
    dependencies=[('orders','0001_initial'),migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations=[
        migrations.CreateModel(name='Payment', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('provider', models.CharField(default='MOCK', max_length=40)), ('provider_reference', models.CharField(blank=True, max_length=100)),
            ('amount', models.DecimalField(decimal_places=2, max_digits=12)), ('status', models.CharField(choices=[('PENDING','In attesa'),('SUCCEEDED','Completato'),('FAILED','Fallito'),('REFUNDED','Rimborsato')], default='PENDING', max_length=20)),
            ('metadata', models.JSONField(blank=True, default=dict)), ('idempotency_key', models.CharField(blank=True, max_length=120, null=True, unique=True)),
            ('created_at', models.DateTimeField(auto_now_add=True)), ('completed_at', models.DateTimeField(blank=True, null=True)),
            ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payments', to='orders.order')),
        ]),
        migrations.CreateModel(name='Invoice', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('number', models.CharField(blank=True, max_length=30, unique=True)), ('status', models.CharField(choices=[('DRAFT','Bozza'),('ISSUED','Emessa'),('CANCELLED','Annullata')], default='DRAFT', max_length=20)),
            ('customer_name', models.CharField(max_length=255)), ('customer_tax_code', models.CharField(blank=True, max_length=30)), ('customer_address', models.CharField(blank=True, max_length=255)),
            ('subtotal', models.DecimalField(decimal_places=2, max_digits=12)), ('vat_total', models.DecimalField(decimal_places=2, max_digits=12)), ('total', models.DecimalField(decimal_places=2, max_digits=12)),
            ('pdf_file', models.FileField(blank=True, upload_to='invoices/%Y/%m/')), ('issued_at', models.DateTimeField(blank=True, null=True)), ('created_at', models.DateTimeField(auto_now_add=True)),
            ('order', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='invoice', to='orders.order')),
        ]),
    ]
