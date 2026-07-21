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
