from django.db import models
from django.contrib.auth.models import User
from django.forms import model_to_dict
# Create your models here.

class TicketStatus(models.TextChoices):
    OPEN = 'OPEN'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE'



class categoria_ticket(models.Model):
    tittle = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(max_length=500, default="", blank=False, null=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='categoria_creado_por')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='categoria_editado_por')

    def __str__(self):
        return "{}-{}".format(self.pk, self.tittle)
    
    def toJSON(self):
        item = model_to_dict(self)
        item['created_by'] = {'id': self.created_by.id, 'usuario': self.created_by.username}
        item['updated_by'] = {'id': self.updated_by.id, 'usuario': self.updated_by.username}
        item['created_at'] = self.created_at.strftime("%Y-%m-%d %H:%M:%S") #agregar la fecha de creacion
        item['updated_at'] = self.updated_at.strftime("%Y-%m-%d %H:%M:%S") #agregar la fecha de actualizacion
        return item
    

def get_user_image_folder(instance, filename):
    return '{0}/{1}/{2}/{3}/{4}'.format('tickets', instance.user_id.username, instance.created_at.year, instance.created_at.month , filename)

class Ticket(models.Model):
    categoria = models.ForeignKey(categoria_ticket, on_delete=models.PROTECT, related_name='ticket_categoria_ticket')
    title = models.CharField(max_length=100,blank=False, null=False)
    assignee_id = models.ForeignKey(User, related_name='ticket_asignado' , null=True, blank=True, on_delete=models.PROTECT)
    status = models.CharField(max_length=25, choices=TicketStatus.choices, default=TicketStatus.OPEN)
    description = models.TextField(max_length=500, default="", blank=False, null=False)
    img_ticket = models.ImageField(upload_to=get_user_image_folder, verbose_name='Image', default='img_defecto.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    user_id = models.ForeignKey(User, related_name='ticket_creador', on_delete=models.PROTECT)
    updated_by = models.ForeignKey(User, related_name='ticket_editado_por', on_delete=models.PROTECT)

    def __str__(self):
        return "{}-{}".format(self.pk, self.title)

    def toJSON(self):
        item = model_to_dict(self) #convertir el objeto a un diccionario
        item['img_ticket'] = self.img_ticket.url #agregar la url de la imagen
        item['categoria'] = {'id': self.categoria.id, 'titulo': self.categoria.tittle} #agregar el id y nombre de la categoria
        item['user_id'] = {'id': self.user_id.id, 'usuario': self.user_id.username} #agregar el id y el username del usuario
        item['updated_by'] = {'id': self.updated_by.id, 'usuario': self.updated_by.username} #agregar el id y nombre de usuario que edita
        if self.assignee_id == None:
            item['assignee_id'] = {'id': None, 'usuario': None}
        else:
            item['assignee_id'] = {'id': self.assignee_id.id, 'usuario': self.assignee_id.username}        
        item['created_at'] = self.created_at.strftime("%Y-%m-%d %H:%M:%S") #agregar la fecha de creacion
        item['updated_at'] = self.updated_at.strftime("%Y-%m-%d %H:%M:%S") #agregar la fecha de actualizacion
        return item

class commentTicket(models.Model):
    title = models.CharField(max_length=100, blank=False, null= False)
    comment = models.TextField(max_length=500, blank=False, null= False)
    id_ticket = models.ForeignKey(Ticket, on_delete=models.PROTECT, related_name='ticket_comment')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='comment_creator', on_delete=models.PROTECT)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='comment_updater', on_delete=models.PROTECT)

    def __str__(self):
        return "{}-{}".format(self.pk, self.title)
    def toJSON(self):
        item = model_to_dict(self)
        item['title'] = self.title
        item['comment']= self.comment
        item['id_ticket'] = {'id': self.id_ticket.pk, 'title': self.id_ticket.title}
        item['created_by'] = {'id': self.created_by.pk, 'usuario': self.created_by.username}
        item['updated_by'] = {'id': self.updated_by.pk, 'usuario': self.updated_by.username}
        item['created_at'] = self.created_at.strftime("%Y-%m-%d %H:%M:%S") 
        item['updated_at'] = self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        return item