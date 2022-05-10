from django.urls import path
from django.conf.urls import url
from rest_framework.authtoken import views
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
    url(r'^signup/', views.RegistroUsuario.as_view(), name='signup'),
    url(r'^update/(?P\d+)/', views.UsuarioDetalle.as_view(), name='update'),
    url(r'^info/(?P\d+)/', views.UsuarioDetalle.as_view(), name='info'),
    url(r'^delete/(?P\d+)/', views.UsuarioDetalle.as_view(), name='delete'),
]
