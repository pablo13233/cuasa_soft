from django.db import models
from apps.usuarios.models import User
from django.forms import model_to_dict
# Create your models here.

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='category_created_by')

    def __str__(self):
        return self.nombre_categoria
    
    def toJSON(self):
        item = model_to_dict(self)
        item['created_by'] = {'id': self.created_by.id, 'username': self.created_by.username}
        return item

class Marca(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_marca = models.CharField(max_length=50)
    image = models.ImageField(upload_to='marcas/', default='img_defecto.jpg', null=True, blank=True, verbose_name='Image')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marca_created_by')

    def __str__(self):
        return self.nombre_marca
    
    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.image.url
        item['created_by'] = {'id': self.created_by.id, 'username': self.created_by.username}
        return item
    
class ModeloItem(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_modelo = models.CharField(max_length=50) 
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modelo_created_by')

    def __str__(self):
        return self.nombre_modelo
    
    def toJSON(self):
        item = model_to_dict(self)
        if self.marca == None:
            item['marca'] = {'id': 0, 'nombre': 'No registrado'}
        else:
            item['marca'] = {'id': self.marca.id, 'nombre': self.marca.nombre_marca}
        item['created_by'] = {'id': self.created_by.id, 'username': self.created_by.username}
        return item

class Proveedor(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_proveedor = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proveedor_created_by')

    def __str__(self):
        return self.nombre_proveedor
    
    def toJSON(self):
        item = model_to_dict(self)
        item['created_by'] = {'id': self.created_by.id, 'username': self.created_by.username}
        return item


class Estado(models.TextChoices):
    ASIGNADO = "ASIGNADO"
    MANTENIMIENTO = "MANTENIMIENTO"
    DESCARTADO = "DESCARTADO"
    DISPONIBLE = "DISPONIBLE"
    GARANTIA = "GARANTIA"


def get_item_image_folder(instance, filename):
    return '{0}/{1}/{2}/{3}'.format('items', instance.categoria.nombre_categoria, instance.correlativo , filename)
class Inventario_Item(models.Model):
    id = models.AutoField(primary_key=True)
    correlativo = models.CharField(max_length=8, unique=True)
    nombre_item = models.CharField(max_length=50, blank=False, null=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='inventario_item_categoria')
    ModeloItem = models.ForeignKey(ModeloItem, on_delete=models.CASCADE, related_name='inventario_item_modelo')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='inventario_item_proveedor')
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) 
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inventario_item_created_by')
    fecha_compra = models.DateField(null=True, blank=True)
    fecha_garantia = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=25, choices=Estado.choices, default=Estado.DISPONIBLE)
    caracteristica = models.TextField(max_length=500, default="", blank=False, null=False)
    comentarios = models.TextField(max_length=500, default="", blank=True, null=True)
    serial_number = models.CharField(max_length=60, blank=False, null=False, unique=True)
    ubicacion = models.TextField(max_length=500, default="", blank=False, null=False)
    imagen_item = models.ImageField(upload_to=get_item_image_folder, default='img_defecto.jpg', null=True, blank=True, verbose_name='Image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.nombre_item
    
    def toJSON(self):
        item = model_to_dict(self)
        item['categoria'] = {'id': self.categoria.id, 'name': self.categoria.nombre_categoria}
        item['ModeloItem'] = {'id': self.ModeloItem.id, 'nombre_modelo': self.ModeloItem.nombre_modelo}
        item['proveedor'] = {'id': self.proveedor.id, 'nombre_proveedor': self.proveedor.nombre_proveedor}
        item['imagen_item']  = self.imagen_item.url
        item['created_by'] = {'id': self.created_by.id, 'username': self.created_by.username}
        item['created_at'] = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        item['updated_at'] = self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        if self.fecha_compra == None:
            item['fecha_compra'] = ''
        else:
            item['fecha_compra'] = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        if self.fecha_garantia == None:
            item['fecha_garantia'] = ''
        else:
            item['fecha_garantia'] = self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        return item


def get_user_notes_assigned_folder(instance, filename):
     return '{0}/{1}/{2}/{3}/{4}'.format('notas_asignacion', instance.user_id.username, instance.created_at.year, instance.created_at.month , filename)

def get_user_notes_unassinged_folder(instance, filename):
     return '{0}/{1}/{2}/{3}/{4}'.format('notas_desasignacion', instance.user_id.username, instance.created_at.year, instance.created_at.month , filename)

class Historial_Asignacion(models.Model):
    id = models.AutoField(primary_key=True) 
    inventario_item = models.ForeignKey(Inventario_Item, on_delete=models.CASCADE, related_name='articulo')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='asignado_a')
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='asignado_por')
    created_at = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creado_por') 
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    observaciones = models.TextField(max_length=500, default="", blank=True, null=True)
    assigned_date = models.DateField(null=True, blank=True)
    unassigned_date = models.DateField(null=True, blank=True)
    nota_asignacion = models.FileField(upload_to=get_user_notes_assigned_folder, null=True, blank=True)
    nota_descargo = models.FileField(upload_to=get_user_notes_unassinged_folder, null=True, blank=True)

    def __str__(self):
        return self.inventario_item.id
    
    def toJSON(self):
        item = model_to_dict(self)
        item['created_by'] = {'id': self.created_by.id, 'username': self.created_by.username}
        item['inventario_item'] = {'id': self.inventario_item.id, 'nombre_item': self.inventario_item.nombre_item}
        item['assigned_by'] = {'id': self.assigned_by.id, 'username': self.assigned_by.username}
        item['assigned_to'] = {'id': self.assigned_to.id,'username': self.assigned_to.username}
        item['created_at'] = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        item['updated_at'] = self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        item['assigned_date'] = self.assigned_date.strftime("%Y-%m-%d %H:%M:%S")
        item['unassigned_date'] = self.unassigned_date.strftime("%Y-%m-%d %H:%M:%S")
        item['nota_asignacion'] = self.nota_asignacion.url
        item['nota_descargo'] = self.nota_descargo.url
        return item

