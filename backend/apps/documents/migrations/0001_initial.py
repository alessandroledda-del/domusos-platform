from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial=True
    dependencies=[('properties','0001_initial'), migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations=[
        migrations.CreateModel(name='Document', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('name', models.CharField(max_length=255)),
            ('document_type', models.CharField(choices=[('DEED','Atto di provenienza'),('CADASTRAL','Visura catastale'),('PLAN','Planimetria catastale'),('MAP','Estratto di mappa'),('ENERGY','APE'),('BUILDING','Titolo edilizio'),('MORTGAGE','Visura ipotecaria'),('OTHER','Altro')], max_length=30)),
            ('file', models.FileField(upload_to='property_documents/%Y/%m/')),
            ('status', models.CharField(choices=[('UPLOADED','Caricato'),('QUEUED','In coda'),('PROCESSING','In elaborazione'),('VERIFIED','Verificato'),('WARNING','Criticità'),('FAILED','Elaborazione fallita')], default='UPLOADED', max_length=20)),
            ('notes', models.TextField(blank=True)), ('extracted_data', models.JSONField(blank=True, default=dict)),
            ('processing_confidence', models.DecimalField(blank=True, decimal_places=3, max_digits=4, null=True)),
            ('processing_error', models.TextField(blank=True)), ('processed_at', models.DateTimeField(blank=True, null=True)),
            ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='properties.property')),
            ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.CreateModel(name='DocumentVersion', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('version_number', models.PositiveIntegerField()), ('file', models.FileField(upload_to='document_versions/%Y/%m/')),
            ('notes', models.TextField(blank=True)), ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='documents.document')),
            ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
        ], options={'ordering':['-version_number'], 'unique_together': {('document','version_number')}}),
    ]
