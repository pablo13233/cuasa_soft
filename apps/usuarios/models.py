from django.db import models
from .managers import UserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.forms import model_to_dict
# Create your models here. 

class User(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)  
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email',]

    objects = UserManager()

    def get_short_name(self):
        return self.username
    
    def get_full_name(self):
        return self.first_name + " " + self.last_name
    
    def __str__(self):
        return self.username

    def toJSON(self):
        item = model_to_dict(self) #convertir el objeto a un diccionario
        item['name'] = self.get_full_name()
        return item