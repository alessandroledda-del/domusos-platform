from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
class Migration(migrations.Migration):
    initial=True
    dependencies=[('properties','0001_initial'), migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations=[
        migrations.CreateModel(name='Case', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('title', models.CharField(max_length=255)), ('service_type', models.CharField(max_length=100)),
            ('status', models.CharField(choices=[('OPEN','Aperta'),('IN_PROGRESS','In lavorazione'),('WAITING','In attesa'),('COMPLETED','Completata'),('CANCELLED','Annullata')], default='OPEN', max_length=20)),
            ('due_date', models.DateField(blank=True, null=True)), ('notes', models.TextField(blank=True)),
            ('created_at', models.DateTimeField(auto_now_add=True)), ('updated_at', models.DateTimeField(auto_now=True)),
            ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_cases', to=settings.AUTH_USER_MODEL)),
            ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_cases', to=settings.AUTH_USER_MODEL)),
            ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cases', to='properties.property')),
        ]),
        migrations.CreateModel(name='Task', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('title', models.CharField(max_length=255)), ('status', models.CharField(choices=[('TODO','Da fare'),('DOING','In corso'),('DONE','Completata')], default='TODO', max_length=10)),
            ('due_date', models.DateField(blank=True, null=True)), ('created_at', models.DateTimeField(auto_now_add=True)),
            ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='workflows.case')),
        ]),
    ]
