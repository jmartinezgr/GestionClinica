from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Campos personalizados
    full_name = models.CharField(max_length=100)
    cedula = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10)
    date_of_birth = models.DateField(default="2000-01-01")
    address = models.CharField(max_length=30)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True)
    

    def __str__(self):
        return self.username

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
