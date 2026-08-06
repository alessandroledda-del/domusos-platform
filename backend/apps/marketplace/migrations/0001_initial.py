from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
class Migration(migrations.Migration):
    initial=True
    dependencies=[('catalog','0001_initial'),('orders','0001_initial'),('workflows','0001_initial'),migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations=[
        migrations.CreateModel(name='PartnerProfile', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('display_name', models.CharField(max_length=255)), ('legal_name', models.CharField(blank=True, max_length=255)), ('vat_number', models.CharField(blank=True, max_length=30)),
            ('professional_type', models.CharField(max_length=100)), ('license_number', models.CharField(blank=True, max_length=100)), ('provinces', models.JSONField(default=list)),
            ('remote_service', models.BooleanField(default=True)), ('description', models.TextField(blank=True)),
            ('status', models.CharField(choices=[('DRAFT','Bozza'),('PENDING','In verifica'),('ACTIVE','Attivo'),('SUSPENDED','Sospeso')], default='DRAFT', max_length=20)),
            ('rating', models.DecimalField(decimal_places=2, default=0, max_digits=3)), ('completed_assignments', models.PositiveIntegerField(default=0)),
            ('average_completion_hours', models.DecimalField(decimal_places=2, default=0, max_digits=10)), ('sla_compliance_rate', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
            ('is_featured', models.BooleanField(default=False)), ('created_at', models.DateTimeField(auto_now_add=True)), ('updated_at', models.DateTimeField(auto_now=True)),
            ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='partner_profile', to=settings.AUTH_USER_MODEL)),
        ], options={'ordering':['-is_featured','-rating','display_name']}),
        migrations.CreateModel(name='PartnerService', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('partner_price', models.DecimalField(decimal_places=2, max_digits=10)), ('estimated_hours', models.PositiveIntegerField(default=24)), ('is_active', models.BooleanField(default=True)),
            ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_offers', to='marketplace.partnerprofile')),
            ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='partner_offers', to='catalog.service')),
        ], options={'unique_together': {('partner','service')}}),
        migrations.CreateModel(name='PartnerAssignment', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('status', models.CharField(choices=[('PROPOSED','Proposta'),('ACCEPTED','Accettata'),('IN_PROGRESS','In lavorazione'),('COMPLETED','Completata'),('REJECTED','Rifiutata'),('CANCELLED','Annullata')], default='PROPOSED', max_length=20)),
            ('agreed_amount', models.DecimalField(decimal_places=2, max_digits=10)), ('commission_rate', models.DecimalField(decimal_places=2, default=20, max_digits=5)),
            ('due_at', models.DateTimeField(blank=True, null=True)), ('accepted_at', models.DateTimeField(blank=True, null=True)), ('completed_at', models.DateTimeField(blank=True, null=True)),
            ('notes', models.TextField(blank=True)), ('created_at', models.DateTimeField(auto_now_add=True)),
            ('assigned_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_partner_assignments', to=settings.AUTH_USER_MODEL)),
            ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partner_assignments', to='workflows.case')),
            ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='partner_assignments', to='orders.order')),
            ('partner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='assignments', to='marketplace.partnerprofile')),
        ], options={'ordering':['-created_at']}),
        migrations.CreateModel(name='Commission', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('gross_amount', models.DecimalField(decimal_places=2, max_digits=10)), ('commission_rate', models.DecimalField(decimal_places=2, max_digits=5)),
            ('platform_amount', models.DecimalField(decimal_places=2, max_digits=10)), ('partner_amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ('status', models.CharField(choices=[('PENDING','In attesa'),('EARNED','Maturata'),('PAID','Pagata'),('CANCELLED','Annullata')], default='PENDING', max_length=20)),
            ('earned_at', models.DateTimeField(blank=True, null=True)), ('created_at', models.DateTimeField(auto_now_add=True)),
            ('assignment', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='commission', to='marketplace.partnerassignment')),
        ]),
        migrations.CreateModel(name='Payout', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('number', models.CharField(blank=True, max_length=30, unique=True)), ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
            ('status', models.CharField(choices=[('DRAFT','Bozza'),('APPROVED','Approvato'),('PAID','Pagato'),('FAILED','Fallito')], default='DRAFT', max_length=20)),
            ('period_start', models.DateField()), ('period_end', models.DateField()), ('notes', models.TextField(blank=True)),
            ('approved_at', models.DateTimeField(blank=True, null=True)), ('paid_at', models.DateTimeField(blank=True, null=True)), ('created_at', models.DateTimeField(auto_now_add=True)),
            ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_partner_payouts', to=settings.AUTH_USER_MODEL)),
            ('partner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payouts', to='marketplace.partnerprofile')),
        ]),
    ]
