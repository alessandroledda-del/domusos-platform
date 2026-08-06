from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial=True
    dependencies=[migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations=[
        migrations.CreateModel(name='Company', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('name', models.CharField(max_length=255)),
            ('vat_number', models.CharField(max_length=20, unique=True)),
            ('company_type', models.CharField(choices=[('AGENCY','Agenzia immobiliare'),('TECHNICAL','Studio tecnico'),('ENTERPRISE','Enterprise'),('PARTNER','Partner')], max_length=20)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
            ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='owned_companies', to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.CreateModel(name='CompanyMembership', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('role', models.CharField(choices=[('ADMIN','Amministratore'),('MANAGER','Responsabile'),('OPERATOR','Operatore'),('VIEWER','Solo lettura')], default='OPERATOR', max_length=20)),
            ('is_active', models.BooleanField(default=True)), ('created_at', models.DateTimeField(auto_now_add=True)),
            ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='companies.company')),
            ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_memberships', to=settings.AUTH_USER_MODEL)),
        ], options={'unique_together': {('company','user')}}),
        migrations.CreateModel(name='CompanyInvitation', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('email', models.EmailField(max_length=254)),
            ('role', models.CharField(choices=[('ADMIN','Amministratore'),('MANAGER','Responsabile'),('OPERATOR','Operatore'),('VIEWER','Solo lettura')], default='OPERATOR', max_length=20)),
            ('token', models.CharField(max_length=64, unique=True)),
            ('status', models.CharField(choices=[('PENDING','In attesa'),('ACCEPTED','Accettato'),('REVOKED','Revocato')], default='PENDING', max_length=20)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
            ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to='companies.company')),
            ('invited_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sent_company_invitations', to=settings.AUTH_USER_MODEL)),
        ], options={'unique_together': {('company','email','status')}}),
    ]
