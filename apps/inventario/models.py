from django.db import models
from apps.usuarios.models import User
from django.forms import model_to_dict
# Create your models here.

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='category_created_by')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']

class Marca(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='marcas/', default='img_defecto.jpg', null=True, blank=True, verbose_name='Image')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marca_created_by')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ['name']

class Proveedor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proveedor_created_by')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['name']

class Tipo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tipo_created_by')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'
        ordering = ['name']

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    correlativo = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='item_categoria')
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='item_marca')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='item_proveedor')
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='item_created_by')
    asignado = models.ForeignKey(User, on_delete=models.CASCADE, related_name='item_asignado', null=True, blank=True)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE, related_name='item_tipo')
    fecha_compra = models.DateField(null=True, blank=True)
    fehca_garantia = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        ordering = ['name']