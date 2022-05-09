from django.urls import path
from . import views

app_name = 'usuarios_app'  # namespace

urlpatterns = [
    path(
        'usuarios/',
        views.UsuariosView.as_view(),
        name='admin_usuarios'
    ),
    path(
        'usuarios/crear-usuario',
        views.RegistroUsuarioCreateView.as_view(),
        name='reg_usuarios'
    ),
]
