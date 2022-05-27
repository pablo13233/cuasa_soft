from distutils import log
from django.shortcuts import render, redirect
from django.views.generic import (
    TemplateView, CreateView, ListView, UpdateView, DeleteView, DetailView,
)
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from apps.usuarios.models import User
from apps.usuarios.forms import RegistroForm
from django.contrib.auth import authenticate
from django.http import JsonResponse


# Create your views here.
@login_required
def Create_User(request):
    if request.method == 'POST':
        check1 = False
        check2 = False
        check3 = False
        form = RegistroForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            if password1 != password2:
                check1 = True
                messages.error(request, 'Las contraseñas no coinciden',
                               extra_tags='alert alert-warning alert-dismissible fade show')
            if User.objects.filter(username=username).exists():
                check2 = True
                messages.error(request, 'El nombre de usuario ya existe',
                               extra_tags='alert alert-warning alert-dismissible fade show')
            if User.objects.filter(email=email).exists():
                check3 = True
                messages.error(request, 'El correo electrónico ya existe',
                               extra_tags='alert alert-warning alert-dismissible fade show')
            if check1 or check2 or check3:
                messages.error(request, 'No se pudo crear el usuario',
                               extra_tags='alert alert-warning alert-dismissible fade show')
                return redirect('usuarios_app:crear_usuarios')
            else:
                user = User.objects.create_user(
                    username=username, password=password1, email=email, first_name=first_name, last_name=last_name
                )
                messages.success(request, f'El usuario {username} se creó correctamente',
                                 extra_tags='alert alert-success alert-dismissible fade show')
                return redirect('usuarios_app:crear_usuarios')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/crear_usuario.html', {'form': form})


@login_required
def Usuario_View(request):
    if request.method == 'POST' and request.is_ajax():
        data = []
        try:
            # ========================   select   =========================
            action = request.POST['action']
            if action == 'buscardatos':
                for i in User.objects.all():
                    data.append(i.toJSON())
            # ========================   Crear   =========================
            elif action == 'crear':
                check1 = False
                check2 = False
                check3 = False
                form = RegistroForm(request.POST)
                if form.is_valid():
                    username = form.cleaned_data['username']
                    password1 = form.cleaned_data['password1']
                    password2 = form.cleaned_data['password2']
                    email = form.cleaned_data['email']
                    first_name = form.cleaned_data['first_name']
                    last_name = form.cleaned_data['last_name']
                    
                    if password1 != password2:
                        check1 = True
                        messages.error(request, 'Las contraseñas no coinciden',
                                    extra_tags='warning')
                    if User.objects.filter(username=username).exists():
                        check2 = True
                        messages.error(request, 'El nombre de usuario ya existe',
                                    extra_tags='warning')
                    if User.objects.filter(email=email).exists():
                        check3 = True
                        messages.error(request, 'El correo electrónico ya existe',
                                    extra_tags='warning')
                    if check1 or check2 or check3:
                        messages.error(request, 'No se pudo crear el usuario',
                                    extra_tags='warning')
                        return redirect('usuarios_app:crear_usuarios')
                    else:
                        user = User.objects.create_user(
                            username=username, password=password1, email=email, first_name=first_name, last_name=last_name
                        )
                        return redirect('usuarios_app:crear_usuarios')
                data = {'tipo_accion': 'crear', 'correcto': True}
                # ========================   desactivar   =========================
            elif action == 'desactivar':
                dato_User = User.objects.get(username=request.POST['username'])
                dato_User.is_active = request.POST['is_active']
                
                dato_User.save()
                data = {'tipo_accion': 'desactivar', 'correcto': True}
            else:
                data['error'] = 'Ha ocurrido un error'

        except Exception as e:
            data['error'] = str(e)
            data = {'tipo_accion': 'error', 'correcto': False, 'error': str(e)}
        return JsonResponse(data, safe=False)
    elif request.method == "GET":
        return render(request, 'usuarios/home_usuarios.html')


class EditarUsuarioView(UpdateView):
    model = User
    template_name = "TEMPLATE_NAME"
    success_url = reverse_lazy('usuarios_app:lista_usuarios')
    login_url = reverse_lazy('login_app:login')
