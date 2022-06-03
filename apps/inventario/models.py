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
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nombre_categoria']

class Marca(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_marca = models.CharField(max_length=50)
    image = models.ImageField(upload_to='marcas/', default='img_defecto.jpg', null=True, blank=True, verbose_name='Image')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marca_created_by')

    def __str__(self):
        return self.nombre_marca
    
    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ['nombre_marca']

class Proveedor(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_proveedor = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proveedor_created_by')

    def __str__(self):
        return self.nombre_proveedor
    
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['nombre_proveedor']

class Tipo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_tipo = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tipo_created_by')

    def __str__(self):
        return self.nombre_tipo
    
    class Meta:
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'
        ordering = ['nombre_tipo']

class Modelo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_modelo = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modelo_created_by')

    def __str__(self):
        return self.nombre_modelo
    
    class Meta:
        verbose_name = 'Modelo'
        verbose_name_plural = 'Modelos'
        ordering = ['nombre_modelo']

class Estado(models.Model):
    id = models.AutoField(primary_key=True)
    name_estado = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='estado_created_by')

    def __str__(self):
        return self.name_estado
    
    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
        ordering = ['name_estado']

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    correlativo = models.CharField(max_length=50, unique=True)
    nombre_item = models.CharField(max_length=50, blank=False, null=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='item_categoria')
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='item_marca')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='item_proveedor')
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='item_created_by')
    asignado = models.ForeignKey(User, on_delete=models.CASCADE, related_name='item_asignado')
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE, related_name='item_tipo')
    fecha_compra = models.DateField(null=True, blank=True)
    fehca_garantia = models.DateField(null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='item_estado')
    caracteristica = models.TextField(max_length=500, default="", blank=False, null=False)
    comentarios = models.TextField(max_length=500, default="", blank=True, null=True)
    serial_number = models.CharField(max_length=60, blank=False, null=False, unique=True)
    ubicacion = models.TextField(max_length=500, default="", blank=False, null=False)

    def __str__(self):
        return self.nombre_item
    
    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items' 
        ordering = ['correlativo']


def get_user_notes_assigned_folder(instance, filename):
     return '{0}/{1}/{2}/{3}/{4}'.format('notas_asignacion', instance.user_id.username, instance.created_at.year, instance.created_at.month , filename)

def get_user_notes_unassinged_folder(instance, filename):
     return '{0}/{1}/{2}/{3}/{4}'.format('notas_desasignacion', instance.user_id.username, instance.created_at.year, instance.created_at.month , filename)

class Historial_Asignacion(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='articulo')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='asignado_a')
    created_at = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creado_por') 
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    update_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actualizado_por')
    observaciones = models.TextField(max_length=500, default="", blank=True, null=True)
    nota_asignacion = models.FileField(upload_to=get_user_notes_assigned_folder, null=True, blank=True)
    nota_descargo = models.FileField(upload_to=get_user_notes_unassinged_folder, null=True, blank=True)

    def __str__(self):
        return self.item.id
    
    class Meta:
        verbose_name = 'Historial_Asignacion'
        verbose_name_plural = 'Historial_Asignaciones'
        ordering = ['fecha_asignacion']