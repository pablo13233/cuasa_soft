from django.shortcuts import render
from django.views.generic import (
    TemplateView, CreateView, ListView,
    )
from django.urls import reverse_lazy

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


class UsuariosView(ListView):
    template_name = "usuarios/home_usuarios.html"
    paginate_by = 10
    ordering = 'first_name'
    context_object_name = 'usuarios'
    model  = User


class RegistroUsuarioCreateView(TemplateView):
    # model = User
    template_name = "usuarios/crear_usuario.html"