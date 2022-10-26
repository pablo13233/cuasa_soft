from enum import unique
from django.db import models
from django.contrib.auth.models import *
from django.forms import model_to_dict
# Create your models here. 

class Departamentos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_depto = models.CharField(max_length=50, unique=True, blank=False, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.nombre_depto
    
    def toJSON(self):
        item = model_to_dict(self)
        item['nombre_depto'] = self.nombre_depto
        item['created_date'] = self.created_date.strftime("%Y-%m-%d %H:%M:%S")
        return item
class Empleado(models.Model):
    dni = models.CharField(primary_key=True, max_length=13, blank=False, null=False)
    email = models.EmailField(max_length=50, unique=True)  
    nombres = models.CharField(max_length=50, blank=True)
    apellidos = models.CharField(max_length=50, blank=True)
    depto = models.ForeignKey(Departamentos, on_delete=models.PROTECT, null=True, blank=True, related_name="departamentos_usuarios")
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False, related_name="empleado_usuario")
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False, related_name="empleado_creado_por")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='empleado_editado_por')
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)
 
    def get_full_name(self):
        return self.nombres + " " + self.apellidos
    
    def __str__(self):
        return '{}-{}-{}'.format(self.dni, self.nombres, self.apellidos)

    def toJSON(self):
        item = model_to_dict(self) #convertir el objeto a un diccionario
        item['nombres'] = self.nombres
        item['apellidos'] = self.apellidos
        item['dni'] = self.dni
        item['email'] = self.email
        item['depto'] = {'id': self.depto.id, 'nombre_depto': self.depto.nombre_depto}
        item['usuario'] = {'id': self.usuario.pk, 'usuario': self.usuario.username}
        if self.usuario.is_active == True:
            item['estado'] = {'estado': 'activo'}
        else:
            item['estado'] = {'estado': 'inactivo'}
        if self.usuario.is_staff == True:
            item['staff'] = {'staff': 'true'}
        else:
            item['staff'] = {'staff': 'false'}
        item['created_by'] = {'id': self.created_by.pk, 'usuario': self.created_by.username}
        item['updated_by'] = {'id': self.updated_by.pk, 'usuario': self.updated_by.username}
        item['created_date'] = self.created_date.strftime("%Y-%m-%d %H:%M:%S") #agregar la fecha de creacion
        item['updated_date'] = self.created_date.strftime("%Y-%m-%d %H:%M:%S") #agregar la fecha de actualizacion
        return item
