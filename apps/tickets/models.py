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
    description = models.TextField(max_length=500, null=True, blank=True)
    img_ticket = models.ImageField(upload_to='tickets/', verbose_name='Image')
    created_at = models.DateTimeField('creado en',auto_now_add=True)
    updated_at = models.DateTimeField('actualizado en',auto_now=True)
    username = models.ForeignKey(User, related_name='creador', on_delete=models.CASCADE)

    def __str__(self):
        return "{}-{}".format(self.pk, self.title)

    def toJSON(self):
        item = model_to_dict(self) #convertir el objeto a un diccionario
        item['img_ticket'] = self.img_ticket.url #agregar la url de la imagen
        return item