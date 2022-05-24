from django.shortcuts import render
from django.views.generic import (
    TemplateView, CreateView, ListView, UpdateView, DeleteView, DetailView,
)
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required

from .models import User
from apps.usuarios.forms import RegistroForm
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class CrearUsuarioView(LoginRequiredMixin, CreateView):
    template_name = "usuarios/crear_usuario.html"
    form_class = RegistroForm
    success_url = reverse_lazy('usuarios_app:crear_usuarios')
    login_url = reverse_lazy('login_app:login')
    def form_valid(self, form):
        User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password2'],
            nombres = form.cleaned_data['nombres'],
            apellidos = form.cleaned_data['apellidos']
        )
        return super(RegistroForm, self).form_valid(form)  


class ListaUsuariosView(LoginRequiredMixin, ListView):
    template_name = "usuarios/home_usuarios.html"
    context_object_name = 'usuarios'
    paginate_by = 10
    ordering = ['nombres']
    model = User
    login_url = reverse_lazy('login_app:login')


class EditarUsuarioView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "TEMPLATE_NAME"
    success_url = reverse_lazy('usuarios_app:lista_usuarios')
    login_url = reverse_lazy('login_app:login')

class EliminarUsuarioView(LoginRequiredMixin, DeleteView):
    model = User
    Template_name = "TEMPLATE_NAME"
    success_url = reverse_lazy('usuarios_app:lista_usuarios')
    login_url = reverse_lazy('login_app:login')

