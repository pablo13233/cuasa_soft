from enum import unique
from django.db import models
from django.contrib.auth.models import User
from apps.inventario.models import Inventario_Item
from django.forms import model_to_dict
# Create your models here.



#def get_user_notes_assigned_folder(instance, filename):
#     return '{0}/{1}/{2}/{3}/{4}'.format('notas_asignacion', instance.user_id.username, instance.created_at.year, instance.created_at.month , filename)

#def get_user_notes_unassinged_folder(instance, filename):
#     return '{0}/{1}/{2}/{3}/{4}'.format('notas_desasignacion', instance.user_id.username, instance.created_at.year, ins tance.created_at.month , filename)

class estado_asignacion(models.TextChoices):
    ASIGNADO = 'ASIGNADO'
    DESCARGO = 'DESCARGO'
    

class historial_asignaciones(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='asignado_a', null=False, blank=False)
    inventario_item = models.ForeignKey(Inventario_Item, on_delete=models.CASCADE, null=False, blank=False )
    status = models.CharField(max_length=25, choices=estado_asignacion.choices, default=estado_asignacion.ASIGNADO)
    assigned_date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name="asigna")
    updated_date = models.DateTimeField(auto_now=True, null=False, blank=False)
    update_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name="actualiza")
    observaciones = models.TextField(max_length=500, default="", blank=True, null=True)

    def __str__(self):
        return self.id

    def  toJSON(self):
        item = model_to_dict(self)
        item['inventario_item']= {'id': self.inventario_item.id, 'correlativo': self.inventario_item.correlativo}
        item['usuario'] = {'id': self.usuario.id,'username': self.usuario.username}
        item['assigned_date'] = self.assigned_date.strftime("%Y-%m-%d")
        item['assigned_by'] = {'id': self.assigned_by.id, 'username': self.assigned_by.username}
        item['updated_date'] = self.updated_date.strftime("%Y-%m-%d")
        item['update_by'] = {'id': self.update_by.id, 'username': self.update_by.username}
        return item