from distutils import log
from django.shortcuts import render, redirect
from django.views.generic import (
    ListView, DetailView, UpdateView,
)
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.auth import authenticate
from apps.usuarios.models import User
from apps.usuarios.forms import RegistroForm, UpdateUserForm, UpdatePasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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


class Usuario_List(LoginRequiredMixin, ListView):
    model = User
    template_name = 'usuarios/home_usuarios.html'
    context_object_name = 'usuarios'
    paginate_by = 10
    order_by = 'id' 

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by(self.order_by)

@login_required
def Update_User(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'El usuario {user.username} se actualizó correctamente',
                             extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('usuarios_app:lista_usuarios')
    else:
        form = UpdateUserForm(instance=user)
    return render(request, 'usuarios/edit_usuario.html', {'form': form})

