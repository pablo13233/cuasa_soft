from django.db import models
from django.contrib.auth.models import User
from django.forms import model_to_dict
# Create your models here.

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='category_created_by')

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
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='marca_created_by')

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
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='modelo_created_by')

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
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='proveedor_created_by')

    def __str__(self):
        return self.nombre_proveedor
    
    def toJSON(self):
        item = model_to_dict(self)
        item['created_by'] = {'id': self.created_by.id, 'username': self.created_by.username}
        return item


class Estado(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_estado = models.CharField(max_length=50, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='estado_created_by')

    def __str__(self):
        return self.nombre_estado
    
    def toJSON(self):
        item = model_to_dict(self)
        item['created_by'] = {'id': self.created_by.id, 'username': self.created_by.username}
        return item


def get_item_image_folder(instance, filename):
    return '{0}/{1}/{2}/{3}'.format('items', instance.categoria.nombre_categoria, instance.correlativo , filename)
class Inventario_Item(models.Model):
    id = models.AutoField(primary_key=True)
    correlativo = models.CharField(max_length=8, unique=True)
    nombre_item = models.CharField(max_length=50, blank=False, null=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='inventario_item_categoria')
    ModeloItem = models.ForeignKey(ModeloItem, on_delete=models.PROTECT, related_name='inventario_item_modelo')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='inventario_item_proveedor')
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) 
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='inventario_item_created_by')
    fecha_compra = models.DateField(null=True, blank=True)
    fecha_garantia = models.DateField(null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT, related_name='inventario_item_estado')
    caracteristica = models.TextField(max_length=500, default="", blank=False, null=False)
    comentarios = models.TextField(max_length=500, default="", blank=True, null=True)
    serial_number = models.CharField(max_length=60, blank=False, null=False, unique=True)
    ubicacion = models.TextField(max_length=500, default="", blank=False, null=False)
    imagen_item = models.ImageField(upload_to=get_item_image_folder, default='img_defecto.jpg', null=True, blank=True, verbose_name='Image')
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name="inventario_item_actualizado_por")

    def __str__(self):
        return self.nombre_item
    
    def toJSON(self):
        item = model_to_dict(self)
        item['categoria'] = {'id': self.categoria.id, 'name': self.categoria.nombre_categoria}
        item['ModeloItem'] = {'id': self.ModeloItem.id, 'nombre_modelo': self.ModeloItem.nombre_modelo}
        item['proveedor'] = {'id': self.proveedor.id, 'nombre_proveedor': self.proveedor.nombre_proveedor}
        item['estado'] = {'id': self.estado.id, 'nombre_estado': self.estado.nombre_estado}
        item['imagen_item']  = self.imagen_item.url
        item['created_by'] = {'id': self.created_by.id, 'username': self.created_by.username}
        item['created_at'] = self.created_at.strftime("%Y-%m-%d")
        item['updated_at'] = self.updated_at.strftime("%Y-%m-%d")
        if self.fecha_compra == None:
            item['fecha_compra'] = ''
        else:
            item['fecha_compra'] = self.fecha_compra.strftime("%Y-%m-%d")
        if self.fecha_garantia == None:
            item['fecha_garantia'] = ''
        else:
            item['fecha_garantia'] = self.fecha_garantia.strftime("%Y-%m-%d")
        if self.updated_by == None:
            item['updated_by'] = {'id': 'no actualizado', 'username': 'no actualizado'}
        else:
            item['updated_by'] = {'id': self.updated_by.id, 'username': self.updated_by.username}
        return item

def get_item_image_folder_maintenance(instance, filename):
    return '{0}/{1}/{2}/{3}'.format('maintenance', instance.inventario_item.correlativo, instance.id, filename)
class historico_mantenimientos(models.Model):
    id = models.AutoField(primary_key=True)
    inventario_item = models.ForeignKey(Inventario_Item, on_delete=models.PROTECT, related_name="mantenimiento_inventario")
    cambio_partes = models.BooleanField(default=False, blank = False, null = False)
    title = models.CharField(max_length=100)
    comentario = models.TextField(max_length=500, blank = False, null = False)
    imagen_mantenimiento = models.ImageField(upload_to=get_item_image_folder_maintenance,default='img_defecto.jpg', blank=False, null = False, verbose_name='Image_Maintenance')
    created_at = models.DateTimeField(auto_now_add=True) 
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='mantenimiento_creado_por')
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name="mantenimiento_actualizado_por")

    def __str__(self):
        return self.title
    
    def toJSON(self):
        item = model_to_dict(self)
        item['inventario'] = {'id': self.inventario_item.id,'correlativo': self.inventario_item.correlativo}
        item['cambio_partes'] = self.cambio_partes
        item['titulo'] = self.title
        item['comentario'] = self.comentario
        item['imagen_mantenimiento'] = self.imagen_mantenimiento.url
        if self.cambio_partes == True:
            item['cambio_partes'] = {'estado': 'si'}
        else:
            item['cambio_partes'] = {'estado': 'no'}
        item['creado_fecha'] = self.created_at.strftime("%Y-%m-%d")
        item['creado_por'] = {'id': self.created_by.id, 'usuario_creo': self.created_by.username}
        item['actualizo_fecha'] = self.created_at.strftime("%Y-%m-%d")
        item['actualizo_por'] = {'id': self.updated_by.id, 'usuario_actualizo': self.updated_by.username}
        return item