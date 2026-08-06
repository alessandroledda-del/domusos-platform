from django.db import migrations, models
import django.db.models.deletion
class Migration(migrations.Migration):
    initial=True
    dependencies=[]
    operations=[
        migrations.CreateModel(name='ServiceCategory', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('code', models.SlugField(max_length=50, unique=True)), ('name', models.CharField(max_length=120)),
            ('description', models.TextField(blank=True)), ('sort_order', models.PositiveIntegerField(default=0)),
            ('is_active', models.BooleanField(default=True)),
        ], options={'ordering':['sort_order','name'], 'verbose_name_plural':'Service categories'}),
        migrations.CreateModel(name='Service', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('code', models.SlugField(max_length=80, unique=True)), ('name', models.CharField(max_length=180)),
            ('short_description', models.CharField(max_length=255)), ('description', models.TextField(blank=True)),
            ('base_price', models.DecimalField(decimal_places=2, max_digits=10)), ('vat_rate', models.DecimalField(decimal_places=2, default=22, max_digits=5)),
            ('sla_hours', models.PositiveIntegerField(default=24)), ('delivery_mode', models.CharField(choices=[('AUTOMATIC','Automatico'),('MANUAL','Manuale'),('HYBRID','Ibrido')], default='MANUAL', max_length=20)),
            ('required_fields', models.JSONField(blank=True, default=list)), ('required_documents', models.JSONField(blank=True, default=list)),
            ('is_active', models.BooleanField(default=True)), ('is_featured', models.BooleanField(default=False)), ('sort_order', models.PositiveIntegerField(default=0)),
            ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='services', to='catalog.servicecategory')),
        ], options={'ordering':['category__sort_order','sort_order','name']}),
    ]
