from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial=True
    dependencies=[('companies','0001_initial'), migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations=[
        migrations.CreateModel(name='Property', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('title', models.CharField(max_length=255)), ('address', models.CharField(max_length=255)),
            ('municipality', models.CharField(max_length=100)), ('province', models.CharField(max_length=2)),
            ('postal_code', models.CharField(blank=True, max_length=10)), ('cadastral_sheet', models.CharField(blank=True, max_length=30)),
            ('cadastral_particle', models.CharField(blank=True, max_length=30)), ('cadastral_subaltern', models.CharField(blank=True, max_length=30)),
            ('cadastral_category', models.CharField(blank=True, max_length=30)), ('domus_score', models.PositiveSmallIntegerField(default=0)),
            ('status', models.CharField(choices=[('DRAFT','Bozza'),('ANALYSIS','In analisi'),('VERIFIED','Verificato'),('ISSUE','Criticità')], default='DRAFT', max_length=20)),
            ('created_at', models.DateTimeField(auto_now_add=True)), ('updated_at', models.DateTimeField(auto_now=True)),
            ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='companies.company')),
            ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.CreateModel(name='Owner', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('first_name', models.CharField(max_length=100)), ('last_name', models.CharField(max_length=100)),
            ('fiscal_code', models.CharField(blank=True, max_length=16)), ('ownership_percentage', models.DecimalField(decimal_places=2, default=100, max_digits=5)),
            ('linked_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_property_records', to=settings.AUTH_USER_MODEL)),
            ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owners', to='properties.property')),
        ]),
    ]
