from django.db import migrations, models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('nome', models.CharField(max_length=100)),
                ('cognome', models.CharField(max_length=100)),
                ('telefono', models.CharField(blank=True, max_length=20, null=True)),
                ('ruolo', models.CharField(choices=[('admin', 'Administrator'), ('user', 'User'), ('guest', 'Guest')], default='user', max_length=50)),
                ('stato', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('suspended', 'Suspended')], default='active', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'users',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ragione_sociale', models.CharField(max_length=255, unique=True)),
                ('partita_iva', models.CharField(max_length=20, unique=True)),
                ('tipo_cliente', models.CharField(choices=[('enterprise', 'Enterprise'), ('pme', 'PME'), ('freelance', 'Freelance'), ('other', 'Other')], max_length=50)),
                ('email', models.EmailField(max_length=255)),
                ('telefono', models.CharField(blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'companies',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('indirizzo', models.CharField(max_length=255)),
                ('comune', models.CharField(max_length=100)),
                ('provincia', models.CharField(max_length=2)),
                ('foglio', models.CharField(max_length=50)),
                ('particella', models.CharField(max_length=50)),
                ('subalterno', models.CharField(blank=True, max_length=50, null=True)),
                ('categoria_catastale', models.CharField(max_length=50)),
                ('domus_score', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('archived', 'Archived')], default='active', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='backend.company')),
            ],
            options={
                'db_table': 'properties',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['email'], name='users_email_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['ruolo'], name='users_ruolo_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['stato'], name='users_stato_idx'),
        ),
        migrations.AddIndex(
            model_name='company',
            index=models.Index(fields=['partita_iva'], name='companies_partita_iva_idx'),
        ),
        migrations.AddIndex(
            model_name='company',
            index=models.Index(fields=['ragione_sociale'], name='companies_ragione_sociale_idx'),
        ),
        migrations.AddIndex(
            model_name='property',
            index=models.Index(fields=['company'], name='properties_company_idx'),
        ),
        migrations.AddIndex(
            model_name='property',
            index=models.Index(fields=['comune'], name='properties_comune_idx'),
        ),
        migrations.AddIndex(
            model_name='property',
            index=models.Index(fields=['provincia'], name='properties_provincia_idx'),
        ),
        migrations.AddIndex(
            model_name='property',
            index=models.Index(fields=['foglio', 'particella'], name='properties_foglio_particella_idx'),
        ),
    ]
