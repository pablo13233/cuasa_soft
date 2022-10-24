from django.urls import path
from django.conf.urls import url
from apps.usuarios import views
from apps.usuarios.views import *

app_name = 'usuarios_app'  # namespace

urlpatterns = [
    # path('usuarios/registro', views.Create_User, name='crear_usuarios'),
    path('usuarios/lista-usuarios', empleados_views, name='empleados'),
    # path('usuarios/editar-usuario/<int:id>', views.Update_User, name='editar_usuarios'),
    path('usuarios/departamentos',departamentosViews, name='departamentos'),
]
