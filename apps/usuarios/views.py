from django.shortcuts import render
from django.views.generic import (
    TemplateView, CreateView, ListView,
)
from django.urls import reverse_lazy

from django.contrib.auth.models import User
from apps.usuarios.forms import RegistroForm

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

# Create your views here.


class RegistroUsuario(APIView):
    # creacion
    def post(self, request, format=None):
        registro = RegistroForm(data=request.data)
        if registro.is_valid():
            registro.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UsuarioDetalle(APIView):
    # detalle
    permissions_classes = (IsAuthenticated,)
    # Index
    def get(self, request, id, format=None, *args, **kwargs):
        usuario = User.objects.get(pk=id)
        userinfo = [{'usuario': usuario.username, 'nombre': usuario.first_name,
                     'apellido': usuario.last_name, 'email': usuario.email}]
        return JsonResponse(userinfo, safe=False)

    permissions_classes = (IsAuthenticated,)
    #update
    def put(self, request, id, *args, **kwargs):
        usuario = User.objects.get(pk=id)
        updateUser = RegistroForm(request.data, instance=usuario) 
        if updateUser.is_valid():
            usuario = updateUser.save()
            pw = usuario.password
            usuario.set_password(pw)
            usuario.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    permissions_classes = (IsAuthenticated,)
    #delete
    def delete(self, request, id):
        usuario  = User.objects.get(pk=id)
        usuario.delete()
        return Response(status=status.HTTP_200_OK)
class UsuariosView(ListView):
    template_name = "usuarios/home_usuarios.html"
    paginate_by = 10
    ordering = 'first_name'
    context_object_name = 'usuarios'
    model = User


class RegistroUsuarioCreateView(CreateView):
    model = User
    template_name = "usuarios/crear_usuario.html"
    form_class = RegistroForm
    success_url = reverse_lazy('usuarios_app:admin_usuarios')
