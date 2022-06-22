from django.db import models
from apps.usuarios.models import User
from django.forms import model_to_dict
# Create your models here.

class TicketStatus(models.TextChoices):
    OPEN = 'OPEN'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE' 

def get_user_image_folder(instance, filename):
    return '{0}/{1}/{2}/{3}/{4}'.format('tickets', instance.user_id.username, instance.created_at.year, instance.created_at.month , filename)

class Ticket(models.Model):
    title = models.CharField(max_length=100)
    assignee_id = models.ForeignKey(User, related_name='asignado' , null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=25, choices=TicketStatus.choices, default=TicketStatus.OPEN)
    description = models.TextField(max_length=500, default="", blank=False, null=False)
    img_ticket = models.ImageField(upload_to=get_user_image_folder, verbose_name='Image', default='img_defecto.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    user_id = models.ForeignKey(User, related_name='creador', on_delete=models.CASCADE)

    def __str__(self):
        return "{}-{}".format(self.pk, self.title)
 
    def toJSON(self):
        item = model_to_dict(self) #convertir el objeto a un diccionario
        item['img_ticket'] = self.img_ticket.url #agregar la url de la imagen
        item['user_id'] = {'id': self.user_id.id, 'usuario': self.user_id.username} #agregar el id y el username del usuario
        if self.assignee_id == None:
            item['assignee_id'] = {'id': None, 'usuario': None}
        else:
            item['assignee_id'] = {'id': self.assignee_id.id, 'usuario': self.assignee_id.username}        
        item['created_at'] = self.created_at.strftime("%Y-%m-%d %H:%M:%S") #agregar la fecha de creacion
        item['updated_at'] = self.updated_at.strftime("%Y-%m-%d %H:%M:%S") #agregar la fecha de actualizacion
        return item