from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        OPERATOR = "OPERATOR", "Operatore DomusOS"
        AGENCY = "AGENCY", "Agenzia"
        TECHNICIAN = "TECHNICIAN", "Tecnico"
        OWNER = "OWNER", "Proprietario"
        CLIENT = "CLIENT", "Cliente"

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CLIENT)
    phone = models.CharField(max_length=30, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
