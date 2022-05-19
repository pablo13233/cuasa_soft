from django.urls import path
from django.conf.urls import url
from apps.usuarios import views

app_name = 'usuarios_app'  # namespace

urlpatterns = [
    path('usuarios/registro', views.CrearUsuarioView.as_view(), name='crear_usuarios'),
    path('usuarios/lista-usuarios', views.ListaUsuariosView.as_view(), name='lista_usuarios'),
    path('usuarios/editar-usuario/<int:pk>', views.EditarUsuarioView.as_view(), name='editar_usuarios'),
    path('usuarios/eliminar-usuario/<int:pk>', views.EliminarUsuarioView.as_view(), name='eliminar_usuarios'),
]
