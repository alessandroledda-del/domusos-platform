from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Custom manager for User model with email as the unique identifier."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('ruolo', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model for the Domusos platform."""

    ROLE_ADMIN = 'admin'
    ROLE_MANAGER = 'manager'
    ROLE_USER = 'user'
    ROLE_GUEST = 'guest'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Administrator'),
        (ROLE_MANAGER, 'Manager'),
        (ROLE_USER, 'User'),
        (ROLE_GUEST, 'Guest'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]

    username = None
    # This project stores names in nome/cognome instead of first_name/last_name.
    first_name = None
    last_name = None

    email = models.EmailField(unique=True, max_length=255)
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    ruolo = models.CharField(max_length=50, choices=ROLE_CHOICES, default='user')
    stato = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'cognome']

    objects = UserManager()

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['ruolo']),
            models.Index(fields=['stato']),
        ]

    def __str__(self):
        return f'{self.nome} {self.cognome} ({self.email})'


class Company(models.Model):
    """Company model for the Domusos platform."""

    CLIENT_TYPE_CHOICES = [
        ('enterprise', 'Enterprise'),
        ('pme', 'PME'),
        ('freelance', 'Freelance'),
        ('other', 'Other'),
    ]

    id = models.AutoField(primary_key=True)
    ragione_sociale = models.CharField(max_length=255, unique=True)
    partita_iva = models.CharField(max_length=20, unique=True)
    tipo_cliente = models.CharField(max_length=50, choices=CLIENT_TYPE_CHOICES)
    email = models.EmailField(max_length=255)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'companies'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['partita_iva']),
            models.Index(fields=['ragione_sociale']),
        ]

    def __str__(self):
        return f'{self.ragione_sociale} ({self.partita_iva})'


class Property(models.Model):
    """Property model for the Domusos platform."""

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('archived', 'Archived'),
    ]

    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='properties')
    indirizzo = models.CharField(max_length=255)
    comune = models.CharField(max_length=100)
    provincia = models.CharField(max_length=2)
    foglio = models.CharField(max_length=50)
    particella = models.CharField(max_length=50)
    subalterno = models.CharField(max_length=50, blank=True, null=True)
    categoria_catastale = models.CharField(max_length=50)
    domus_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'properties'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['company']),
            models.Index(fields=['comune']),
            models.Index(fields=['provincia']),
            models.Index(fields=['foglio', 'particella']),
        ]

    def __str__(self):
        return f'{self.indirizzo}, {self.comune} ({self.provincia})'
