from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
class Migration(migrations.Migration):
    initial=True
    dependencies=[('properties','0001_initial'),migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations=[
        migrations.CreateModel(name='VerificationRun', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('status', models.CharField(choices=[('RUNNING','In esecuzione'),('COMPLETED','Completata'),('FAILED','Fallita')], default='RUNNING', max_length=20)),
            ('score', models.PositiveSmallIntegerField(default=0)), ('passed_rules', models.PositiveIntegerField(default=0)), ('warning_rules', models.PositiveIntegerField(default=0)), ('failed_rules', models.PositiveIntegerField(default=0)),
            ('engine_version', models.CharField(default='0.8', max_length=30)), ('summary', models.JSONField(blank=True, default=dict)), ('started_at', models.DateTimeField(auto_now_add=True)), ('completed_at', models.DateTimeField(blank=True, null=True)),
            ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verification_runs', to='properties.property')),
            ('requested_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
        ], options={'ordering':['-started_at']}),
        migrations.CreateModel(name='Finding', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('rule_code', models.CharField(max_length=100)), ('title', models.CharField(max_length=255)), ('description', models.TextField()),
            ('severity', models.CharField(choices=[('INFO','Informazione'),('LOW','Bassa'),('MEDIUM','Media'),('HIGH','Alta'),('CRITICAL','Critica')], max_length=20)),
            ('status', models.CharField(choices=[('OPEN','Aperta'),('ACKNOWLEDGED','Presa in carico'),('RESOLVED','Risolta'),('ACCEPTED_RISK','Rischio accettato')], default='OPEN', max_length=20)),
            ('evidence', models.JSONField(blank=True, default=dict)), ('resolution_notes', models.TextField(blank=True)), ('resolved_at', models.DateTimeField(blank=True, null=True)), ('created_at', models.DateTimeField(auto_now_add=True)),
            ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compliance_findings', to='properties.property')),
            ('resolved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resolved_compliance_findings', to=settings.AUTH_USER_MODEL)),
            ('verification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='findings', to='compliance.verificationrun')),
        ], options={'ordering':['severity','created_at']}),
        migrations.CreateModel(name='VerificationCertificate', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('public_code', models.CharField(blank=True, max_length=40, unique=True)), ('status', models.CharField(choices=[('VALID','Valido'),('REVOKED','Revocato'),('EXPIRED','Scaduto')], default='VALID', max_length=20)),
            ('verified_level', models.CharField(max_length=30)), ('score', models.PositiveSmallIntegerField()), ('snapshot', models.JSONField(default=dict)),
            ('pdf_file', models.FileField(blank=True, upload_to='verification_certificates/%Y/%m/')), ('issued_at', models.DateTimeField(auto_now_add=True)), ('expires_at', models.DateTimeField(blank=True, null=True)),
            ('revoked_at', models.DateTimeField(blank=True, null=True)), ('revocation_reason', models.TextField(blank=True)),
            ('issued_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ('property', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='verification_certificates', to='properties.property')),
            ('verification', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='certificate', to='compliance.verificationrun')),
        ]),
    ]
