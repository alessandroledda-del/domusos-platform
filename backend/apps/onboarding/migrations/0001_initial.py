from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
class Migration(migrations.Migration):
    initial=True
    dependencies=[migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations=[migrations.CreateModel(name='OnboardingProgress', fields=[
        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        ('organization_created', models.BooleanField(default=False)), ('profile_completed', models.BooleanField(default=False)),
        ('first_property_created', models.BooleanField(default=False)), ('first_document_uploaded', models.BooleanField(default=False)),
        ('first_service_ordered', models.BooleanField(default=False)), ('first_verification_run', models.BooleanField(default=False)),
        ('completed', models.BooleanField(default=False)), ('dismissed', models.BooleanField(default=False)),
        ('metadata', models.JSONField(blank=True, default=dict)), ('updated_at', models.DateTimeField(auto_now=True)),
        ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='onboarding_progress', to=settings.AUTH_USER_MODEL)),
    ])]
