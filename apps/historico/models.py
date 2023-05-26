from django.db import models
from django.contrib.auth.models import User
from django.forms import model_to_dict
# Create your models here.

class historico(models.Model):
    id = models.AutoField(primary_key=True)
    accion = models.TextField(max_length=500, blank=False, null=False)
    tipo_accion = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='historico_created_by')

    def __str__(self):
        return self.accion
    
    def toJSON(self):
        item = model_to_dict(self)
        item['accion'] = self.accion
        if self.tipo_accion == True:
            item['tipo_accion'] = {'tipo': 'INSERTAR'}
        else:
            item['tipo_accion'] = {'tipo': 'MODIFICAR'}
        item['created_at'] = self.created_at.strftime("%Y-%m-%d")
        item['created_by'] = {'id': self.created_by.id, 'username': self.created_by.username}
        return item