from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone


class User(models.Model):
    """User model for the Domusos platform"""
    
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('user', 'User'),
        ('guest', 'Guest'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]
    
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, max_length=255)
    password_hash = models.CharField(max_length=255)
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    ruolo = models.CharField(max_length=50, choices=ROLE_CHOICES, default='user')
    stato = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['ruolo']),
            models.Index(fields=['stato']),
        ]
    
    def __str__(self):
        return f"{self.nome} {self.cognome} ({self.email})"
    
    def set_password(self, raw_password):
        """Hash and set the password"""
        self.password_hash = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Check if the provided password matches the hash"""
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password_hash)


class Company(models.Model):
    """Company model for the Domusos platform"""
    
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
        return f"{self.ragione_sociale} ({self.partita_iva})"


class Property(models.Model):
    """Property model for the Domusos platform"""
    
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
        return f"{self.indirizzo}, {self.comune} ({self.provincia})"
