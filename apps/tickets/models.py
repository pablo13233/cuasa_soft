from django.db import models
from django.contrib.auth.models import User
from django.forms import model_to_dict
# Create your models here.

class TicketStatus(models.TextChoices):
    OPEN = 'Abierto'
    IN_PROGRESS = 'En progreso'
    IN_REVIEW = 'En revisión'
    DONE = 'Terminado'

class Ticket(models.Model):
    title = models.CharField(max_length=100)
    assignee = models.ForeignKey(User, related_name='asignado' , null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=25, choices=TicketStatus.choices, default=TicketStatus.OPEN)
    description = models.TextField(max_length=500, default="", blank=False, null=False)
    img_ticket = models.ImageField(upload_to='tickets/', verbose_name='Image', default='img_defecto.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    user_id = models.ForeignKey(User, related_name='creador', on_delete=models.CASCADE)

    def __str__(self):
        return "{}-{}".format(self.pk, self.title)

    def toJSON(self):
        item = model_to_dict(self) #convertir el objeto a un diccionario
        item['img_ticket'] = self.img_ticket.url #agregar la url de la imagen
        item['user_id'] = {'id': self.user_id.id, 'usuario': self.user_id.username} #agregar el id y el username del usuario
        item['created_at'] = self.created_at.strftime("%Y-%m-%d %H:%M:%S") #agregar la fecha de creacion
        return item