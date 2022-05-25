from django.urls import path
from django.conf.urls import url
from apps.usuarios import views

app_name = 'usuarios_app'  # namespace

urlpatterns = [
    path('usuarios/registro', views.Create_User, name='crear_usuarios'),
    path('usuarios/lista-usuarios', views.Usuario_View, name='lista_usuarios'),
    path('usuarios/editar-usuario/<int:pk>', views.EditarUsuarioView.as_view(), name='editar_usuarios'),
]
