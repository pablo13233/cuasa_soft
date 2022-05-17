from django.db import models

from django.contrib.auth.models import AbstractUser, PermissionsMixin
# Create your models here. 

class User(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)  
    nombres = models.CharField(max_length=50, blank=True)
    apellidos = models.CharField(max_length=50, blank=True)
    
    USERNAME_FIELD = 'username'

    def get_short_name(self):
        return self.username
    
    def get_full_name(self):
        return self.nombres + " " + self.apellidos