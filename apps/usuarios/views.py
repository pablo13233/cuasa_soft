from distutils import log
from django.shortcuts import render, redirect
from django.views.generic import (
    ListView, DetailView, UpdateView,
)
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission, Group
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from apps.usuarios.models import Departamentos, Empleado
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from datetime import datetime


@login_required
def empleados_views(request):
    if request.method == 'POST' and request.is_ajax():
        data = []
        try:
            # =====================  select ================
            action = request.POST['action']
            user_crea = request.user.id
            updated_time = datetime.now()
            if action == 'buscardatos':
                for i in Empleado.objects.all():
                    data.append(i.toJSON())

            # ======================== crear =========================
            elif action == 'crear':

                if (User.objects.filter(username = request.POST['nombre_usuario']).exists()):
                    # nombre de usuario ya existe
                    response = JsonResponse({"message":"El nombre de usuario ya existe"})
                    response.status_code = 500
                    return response
                elif (Empleado.objects.filter(dni = request.POST['dni']).exists()):
                    # el numero de identidad ya esta en usuario
                    response = JsonResponse({"message":"El numero de identidad ya esta usado"})
                    response.status_code = 500
                    return response
                elif (User.objects.filter(email = request.POST['correo']).exists()):
                    # el correo ya existe
                    response = JsonResponse({"message":"El correo ya esta en uso"})
                    response.status_code = 500
                    return response
                elif(request.POST['contrasena2'] != request.POST['contrasena']):
                    #contrasena erronea
                    response = JsonResponse({"message":"Las contraseñas no coinciden"})
                    response.status_code = 500
                    return response
                else:
                    # --------------- Usuario --------------
                    if (request.POST['staff'] == 'false'):
                        n_is_staff = False
                    elif (request.POST['staff'] == 'true'):
                        n_is_staff = True
                    if (request.POST['active'] == 'false'):
                        n_is_active = False
                    elif (request.POST['active'] == 'true'):
                        n_is_active = True
                    n_is_superuser = False
                    
                    User.objects.create_user(
                        username = request.POST['nombre_usuario'],
                        email = request.POST['correo'],
                        first_name = request.POST['nombres'],
                        last_name = request.POST['apellidos'],
                        password = request.POST['contrasena2'],
                        is_staff = n_is_staff,
                        is_active = n_is_active,
                        is_superuser = n_is_superuser,
                    )
                
                    #---------------Empleado-----------------
                    emp = Empleado()
                    emp.dni = request.POST['dni']
                    if int(request.POST['depto'])>0:
                        emp.depto = Departamentos.objects.get(id=request.POST['depto'])
                    if int(user_crea) > 0:
                        emp.created_by = User.objects.get(pk=user_crea)
                    if int(user_crea) > 0:
                        emp.updated_by = User.objects.get(pk=user_crea)
                    emp.usuario = User.objects.get(username = request.POST['nombre_usuario'])
                    emp.save()

                    data = {'tipo_accion': 'crear', 'correcto': True}
                
            elif action == 'editar':
                #---------------Empleado-----------------
                depto = request.POST['depto']
                if int(depto) > 0:
                    u_depto = Departamentos.objects.get(id=depto)
                
                Empleado.objects.filter(dni=request.POST['dni']).update(
                    dni = request.POST['dni'],
                    updated_date = updated_time,
                    updated_by = User.objects.get(pk=user_crea), 
                    depto = u_depto
                )
                # --------------- Usuario --------------
                if (request.POST['staff'] == 'false'):
                    u_is_staff = False
                elif (request.POST['staff'] == 'true'):
                    u_is_staff = True
                User.objects.filter(username = request.POST['nombre_usuario']).update(
                    email = request.POST['correo'],
                    first_name = request.POST['nombres'],
                    last_name = request.POST['apellidos'],
                    is_staff = u_is_staff,
                )

                #agregar upcion de solo activar y cambiar password
                data = {'tipo_accion': 'editar', 'correcto': True}
            elif action == 'desactivar_user':
                 
                User.objects.filter(username = request.POST['nombre_usuario']).update(is_active=False)

                data = {'tipo_accion': 'desactivar_user', 'correcto': True}
            elif action == 'activar_user':
                 
                User.objects.filter(username = request.POST['nombre_usuario']).update(is_active=True)

                data = {'tipo_accion': 'activar_user', 'correcto': True}
            elif action == 'cambiar_psw':
                contrasena1 = request.POST['p_contrasena']
                contrasena2 = request.POST['p_contrasena2']
                
                if contrasena2 == contrasena1:
                    User.objects.filter(username = request.POST['nombre_usuario']).update(password = make_password(contrasena2))

                data = {'tipo_accion': 'cambiar_psw', 'correcto': True}
            else:
                data['error'] = 'Ha ocurrido un error.'
        except Exception as e:
            print("==================== ",str(e))
            # print(action)
            data['error'] = str(e)
            data = {'tipo_accion': 'error',  'correcto': True}
        return JsonResponse(data, safe=False)
    elif request.method == 'GET':
        deptos = Departamentos.objects.all()
        return render(request, 'usuarios/home_usuarios.html',{'departamentos': deptos})

@login_required
def departamentosViews(request):
    if request.method == 'POST' and request.is_ajax():
        data = []
        try:
            # =====================  select ================
            action = request.POST['action']
            id_user = request.user.id
            updated_time = datetime.now()
            if action == 'buscardatos':
                for i in Departamentos.objects.all():
                    data.append(i.toJSON())

            # ======================== crear =========================
            elif action == 'crear':
                dep = Departamentos()
                dep.nombre_depto = request.POST['nombre_depto']
                dep.save()
                print('lol')
                data = {'tipo_accion': 'crear', 'correcto': True}
            elif action == 'editar':
                Departamentos.objects.filter(pk=request.POST['id']).update(
                    nombre_depto = request.POST['nombre_depto'],
                    updated_date = updated_time
                )

                data = {'tipo_accion': 'editar', 'correcto': True}
            else:
                data['error'] = 'Ha ocurrido un error.'
        except Exception as e:
            print(str(e))
            print(action)
            data['error'] = str(e)
            data = {'tipo_accion': 'error',  'correcto': True}
        return JsonResponse(data, safe=False)
    elif request.method == 'GET':
        return render(request, 'usuarios/departamentos.html',{'titulo': 'Inicio', 'entidad':'Creacion de Departamentos'})

@login_required
def permisos_view(request):
    if request.method == 'POST' and request.is_ajax():
        data = []
        try:
            # =====================  select ================
            action = request.POST['action']
            id_user = request.user.id
            updated_time = datetime.now()
            if action == 'buscardatos':
                for i in User.objects.all():
                    data. append(i.toJSON())

            # ======================== crear =========================
            elif action == 'crear':
                # dep = Departamentos()
                # dep.nombre_depto = request.POST['nombre_depto']
                # dep.save()
                # print('lol')
                data = {'tipo_accion': 'crear', 'correcto': True}
            elif action == 'editar':
                # Departamentos.objects.filter(pk=request.POST['id']).update(
                #     nombre_depto = request.POST['nombre_depto'],
                #     updated_date = updated_time
                # )

                data = {'tipo_accion': 'editar', 'correcto': True}
            else:
                data['error'] = 'Ha ocurrido un error.'
        except Exception as e:
            print(str(e))
            print(action)
            data['error'] = str(e)
            data = {'tipo_accion': 'error',  'correcto': True}
        return JsonResponse(data, safe=False)
    elif request.method == 'GET':
        permisos = Permission.objects.all()
        return render(request, 'usuarios/permisos.html',{'permisos': permisos})

@login_required
def grupos_view(request):
    if request.method == 'POST' and request.is_ajax():
        data = []
        try:
            # =====================  select ================
            action = request.POST['action']
            # id_user = request.user.id
            if action == 'buscardatos':
                for i in Group.objects.all():
                    data. append(i.toJSON())

            # ======================== crear =========================
            elif action == 'crear':
                #obtenemos datos de grupo y lista de permisos
                nombre_grupo = request.POST['nombre']
                permission_ids = request.POST['permission_ids[]']
                #creamos el grupo
                group = Group.objects.create(name=nombre_grupo)
                #asignamos permisos al grupo
                for permission_id in permission_ids:
                    permission = Permission.objects.get(permission_id=permission_id)
                    group.permissions.add(permission)
                #guardamos cambios en la base de datos
                group.save()

                data = {'tipo_accion': 'crear', 'correcto': True}
            elif action == 'editar':
                # Departamentos.objects.filter(pk=request.POST['id']).update(
                #     nombre_depto = request.POST['nombre_depto'],
                #     updated_date = updated_time
                # )

                data = {'tipo_accion': 'editar', 'correcto': True}
            else:
                data['error'] = 'Ha ocurrido un error.'
        except Exception as e:
            print(str(e))
            print(action)
            data['error'] = str(e)
            data = {'tipo_accion': 'error',  'correcto': True}
        return JsonResponse(data, safe=False)
    elif request.method == 'GET':
        permisos = Permission.objects.all()
        return render(request, 'usuarios/grupos.html',{'permisos': permisos})