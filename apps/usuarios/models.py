from enum import unique
from django.db import models
from .managers import UserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.forms import model_to_dict
# Create your models here. 

class Departamentos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_depto = models.CharField(max_length=50, unique=True, blank=False, null=False)
    created_date = models.DateField(auto_now_add=True, blank=False, null=False)
    updated_date = models.DateField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.nombre_depto
    
    def toJSON(self):
        item = model_to_dict(self)
        item['nombre_depto'] = self.nombre_depto
        item['updated_date'] =  self.updated_date.strftime("%Y-%m-%d")
        item['created_date'] = self.created_date.strftime("%Y-%m-%d")
        return item
class User(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)  
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    dni = models.CharField(max_length=13, blank=False, null=False)
    depto = models.ForeignKey(Departamentos, on_delete=models.CASCADE, null=True, blank=True, related_name="departamentos_usuarios")
    
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
        item['dni'] = self.dni
        return item
