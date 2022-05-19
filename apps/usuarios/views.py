from django.shortcuts import render
from django.views.generic import (
    TemplateView, CreateView, ListView,
)
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required

from .models import User
from apps.usuarios.forms import RegistroForm


# Create your views here.

""" @login_required
def UsuariosView(request):
    if request.method == 'POST' and request.is_ajax():
        data = []
        try:
            action = request.POST['action']
            if action == 'listar':
                for i in User.objects.all():
                    data.append(i.toJson())
            elif action == 'crear':
                us = User()
                us.username = request.POST['username']
                us.first_name = request.POST['first_name']
                us.last_name = request.POST['last_name']
                us.email = request.POST['email']
                us.set_password(request.POST['password'])
                us.save()

                data = {'tipo_accion': 'crear', 'correcto': True}
            elif action == 'editar':
                us = User.objects.get(id=request.POST['id'])
                us.username = request.POST['username']
                us.first_name = request.POST['first_name']
                us.last_name = request.POST['last_name']
                us.email = request.POST['email']
                us.set_password(request.POST['password'])
                us.save()

                data = {'tipo_accion': 'editar', 'correcto': True}
            elif action == 'eliminar':
                usr = User.objects.get(id=request.POST['id'])
                usr.delete()

                data = {'tipo_accion': 'eliminar', 'correcto': True}
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
            data = {'tipo_accion': 'error', 'correcto': False, 'error': str(e)}
        return JsonResponse(data, safe=False)
    elif request.method == 'GET':
        print("Metodo Normal")
        return render(request, 'usuarios/home_usuarios.html',{'titulo': 'Inicio', 'entidad': 'Usuarios'}) """
            

@login_required
class CrearUsuarioView(CreateView):
    template_name = "usuarios/crear_usuario.html"
    form_class = RegistroForm
    success_url = 'usuarios_app:crear_usuarios'
    
    def form_valid(self, form):
        User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombres = form.cleaned_data['nombres'],
            apellidos = form.cleaned_data['apellidos'],
            is_staff = form.cleaned_data['staff'],
            is_superuser = form.cleaned_data['superuser'],
            is_active = form.cleaned_data['activo']

        )
        return super(RegistroForm, self).form_valid(form)