from django.db import models
from apps.usuarios.models import User
from apps.inventario.models import Inventario_Item
from django.forms import model_to_dict
# Create your models here.



#def get_user_notes_assigned_folder(instance, filename):
#     return '{0}/{1}/{2}/{3}/{4}'.format('notas_asignacion', instance.user_id.username, instance.created_at.year, instance.created_at.month , filename)

#def get_user_notes_unassinged_folder(instance, filename):
#     return '{0}/{1}/{2}/{3}/{4}'.format('notas_desasignacion', instance.user_id.username, instance.created_at.year, instance.created_at.month , filename)

class control_Asignaciones(models.Model):
    id = models.AutoField(primary_key=True) 
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='asignado_a')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creado_por')
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    update_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actualizado por')
    observaciones = models.TextField(max_length=500, default="", blank=True, null=True)

    def __str__(self):
        return self.inventario_item.id
    
    def toJSON(self):
        item = model_to_dict(self)
        item['created_by'] = {'id': self.created_by.id, 'username': self.created_by.username}
        item['assigned_by'] = {'id': self.assigned_by.id, 'username': self.assigned_by.username}
        item['usuario'] = {'id': self.assigned_to.id,'username': self.assigned_to.username}
        item['assigned_at'] = self.assigned_at.strftime("%Y-%m-%d")
        item['updated_at'] = self.updated_at.strftime("%Y-%m-%d")
        return item