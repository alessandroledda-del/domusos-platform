from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
class Migration(migrations.Migration):
    initial=True
    dependencies=[('catalog','0001_initial'),('companies','0001_initial'),('properties','0001_initial'),migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations=[
        migrations.CreateModel(name='Order', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('number', models.CharField(blank=True, max_length=30, unique=True)),
            ('status', models.CharField(choices=[('DRAFT','Bozza'),('AWAITING_PAYMENT','In attesa di pagamento'),('PAID','Pagato'),('IN_PROGRESS','In lavorazione'),('WAITING_CUSTOMER','In attesa del cliente'),('COMPLETED','Completato'),('CANCELLED','Annullato'),('REFUNDED','Rimborsato')], default='DRAFT', max_length=30)),
            ('customer_notes', models.TextField(blank=True)), ('internal_notes', models.TextField(blank=True)),
            ('service_data', models.JSONField(blank=True, default=dict)), ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
            ('vat_total', models.DecimalField(decimal_places=2, default=0, max_digits=12)), ('total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
            ('sla_due_at', models.DateTimeField(blank=True, null=True)), ('paid_at', models.DateTimeField(blank=True, null=True)), ('completed_at', models.DateTimeField(blank=True, null=True)),
            ('created_at', models.DateTimeField(auto_now_add=True)), ('updated_at', models.DateTimeField(auto_now=True)),
            ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='companies.company')),
            ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ('property', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='properties.property')),
        ], options={'ordering':['-created_at']}),
        migrations.CreateModel(name='OrderItem', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('description', models.CharField(max_length=255)), ('quantity', models.PositiveIntegerField(default=1)),
            ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)), ('vat_rate', models.DecimalField(decimal_places=2, max_digits=5)),
            ('sla_hours', models.PositiveIntegerField(default=24)), ('delivery_notes', models.TextField(blank=True)),
            ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order')),
            ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.service')),
        ]),
        migrations.CreateModel(name='OrderStatusEvent', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('previous_status', models.CharField(blank=True, max_length=30)), ('new_status', models.CharField(max_length=30)),
            ('note', models.TextField(blank=True)), ('created_at', models.DateTimeField(auto_now_add=True)),
            ('changed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_events', to='orders.order')),
        ], options={'ordering':['created_at']}),
    ]
