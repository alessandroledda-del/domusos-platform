from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='ruolo',
            field=models.CharField(
                choices=[
                    ('admin', 'Administrator'),
                    ('manager', 'Manager'),
                    ('user', 'User'),
                    ('guest', 'Guest'),
                ],
                default='user',
                max_length=50,
            ),
        ),
    ]
