from django.urls import path
from django.conf.urls import url
from apps.usuarios.views import *

app_name = 'usuarios_app'  # namespace

urlpatterns = [
    path('usuarios/ajax', UsuariosView, name='admin_usuarios'),
    # path('usuarios/crear-usuario', RegistroUsuarioCreateView, name='reg_usuarios'),
]
