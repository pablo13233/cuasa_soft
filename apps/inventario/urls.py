from django.urls import path
from apps.inventario.views import *

app_name = 'inventario_app' # namespace

urlpatterns = [
    path('inventario', inventarioViews, name='inventario'),
    #catalogos / parametros
    path('inventario/categorias/', categoriaViews, name='categorias'),
    path('inventario/marcas/', marcasViews, name='marcas'),
    path('inventario/modelo/', modeloViews, name='modelo'),
    path('inventario/proveedores/', proveedoresViews, name='proveedores'),
    path('inventario/estados/', estadosViews, name='estados'),
    path('inventario/descarte/', descarteViews, name='descarte'),
    path('inventario/descarte-pdf/', pdfInventarioView, name='nota_descarte'),
    path('inventario/mantenimiento/', mantenimientosViews, name='mantenimiento'),
    path('inventario/mantenimiento-pdf/', pdfMantenimientoView, name='nota_mantenimiento'),
]