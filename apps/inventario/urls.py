from django.urls import path
from apps.inventario.views import *

app_name = 'inventario_app' # namespace

urlpatterns = [
    path('inventario', inventarioViews, name='inventario'),
    #catalogos / parametros
    path('categorias/', categoriaViews, name='categorias'),
    path('marcas/', marcasViews, name='marcas'),
]