from distutils import log
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.hashers import make_password
from apps.usuarios.models import Departamentos, Empleado
from apps.asignaciones.models import historial_asignaciones
from apps.tickets.models import Ticket
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import transaction
from django.utils import timezone

def error_view(request):
    return render(request, 'partials/error_permisos.html')

@login_required
def empleados_views(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.has_perm('usuarios.view_empleado')):
        return redirect('usuarios_app:error_view')
    if request.method == 'POST' and request.is_ajax():
        data = []
        try:
            with transaction.atomic():
            # =====================  select ================
                action = request.POST['action']
                user_crea = request.user.id
                updated_time = timezone.now()
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
                    elif(request.POST['id_grupo'] == 0):
                        response = JsonResponse({"message":"Seleccione un grupo"})
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
                        usuario_grupo = User.objects.get(username=request.POST['nombre_usuario']) #Obtenemos el usuario que acabamos de crear
                        grupo_user = Group.objects.get(id=request.POST['id_grupo']) #Obtenemos el grupo al que queremos agregar el usuario
                        usuario_grupo.groups.add(grupo_user) #agregamos el usuario al grupo
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
                elif action == 'grupo_usuario':
                    username = request.POST['username']
                    # print('usuario: ',username)
                    usuario = User.objects.get(username = username) #obtenemos usuario
                    grupo_data = []
                    nombre = usuario.first_name #obtenemos nombre del usuario
                    grupo_data.append(nombre)
                    apellido = usuario.last_name #obtenemos apellido del usuario
                    grupo_data.append(apellido) #agregamos la data a el diccionario
                    # print('data usuario: ',grupo_data)
                    grupos = usuario.groups.all()
                    for ug in grupos:
                        grupo = ug.pk
                        grupo_data.append(grupo)
                    # print('data usuario: ',grupo_data)
                    response = JsonResponse(grupo_data, safe=False)
                    return response
                elif action == 'editar':
                    #validaciones para que no se actualizen datos en blanco
                    if len(request.POST['dni']) == 0:
                        # el numero de identidad ya esta en usuario
                        response = JsonResponse({"message":"No puede dejar el numero de identidad en blanco"})
                        response.status_code = 500
                        return response
                    elif len(request.POST['correo']) == 0:
                        # el correo ya existe
                        response = JsonResponse({"message":"No puede dejar el correo en blanco"})
                        response.status_code = 500
                        return response
                    elif len(request.POST['apellidos']) == 0:
                        #contrasena erronea
                        response = JsonResponse({"message":"No puede dejar el apellido en blanco"})
                        response.status_code = 500
                        return response
                    elif len(request.POST['nombres']) == 0:
                        #contrasena erronea
                        response = JsonResponse({"message":"No puede dejar el nombre en blanco"})
                        response.status_code = 500
                        return response
                    elif int(request.POST['id_grupo']) == 0:
                        response = JsonResponse({"message":"Seleccione un grupo"})
                        response.status_code = 500
                        return response
                    elif int(request.POST['depto']) == 0:
                        response = JsonResponse({"message":"Seleccione un departamento"})
                        response.status_code = 500
                        return response
                    else:
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
                        # -------------------- grupo --------------------
                        usuario_grupo = User.objects.get(username=request.POST['nombre_usuario']) #Obtenemos el usuario que acabamos de crear
                        grupo_user = request.POST['id_grupo']
                        
                        usuario_grupo.groups.set(grupo_user) #agregamos el usuario al grupo
                        
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
            # print("==================== ",str(e))
            # print(action)
            data['error'] = str(e)
            data = {'tipo_accion': 'error',  'correcto': True}
            transaction.rollback()
        else:
            transaction.commit()
        return JsonResponse(data, safe=False)
    elif request.method == 'GET':
        deptos = Departamentos.objects.all()
        grupos = Group.objects.all()
        return render(request, 'usuarios/home_usuarios.html',{'departamentos': deptos, 'grupos':grupos})

@login_required
def departamentosViews(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.has_perm('usuarios.view_departamentos')):
        return redirect('usuarios_app:error_view')
    if request.method == 'POST' and request.is_ajax():
        data = []
        try:
            with transaction.atomic():
                # =====================  select ================
                action = request.POST['action']
                id_user = request.user.id
                updated_time = timezone.now()
                if action == 'buscardatos':
                    for i in Departamentos.objects.all():
                        data.append(i.toJSON())

                # ======================== crear =========================
                elif action == 'crear':
                    dep = Departamentos()
                    dep.nombre_depto = request.POST['nombre_depto']
                    dep.save()
                    # print('lol')
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
            # print(str(e))
            # print(action)
            data['error'] = str(e)
            data = {'tipo_accion': 'error',  'correcto': True}
            transaction.rollback()
        else:
            transaction.commit()
        return JsonResponse(data, safe=False)
    elif request.method == 'GET':
        return render(request, 'usuarios/departamentos.html',{'titulo': 'Inicio', 'entidad':'Creacion de Departamentos'})

@login_required
def grupos_view(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.has_perm('usuarios.view_group')):
        return redirect('usuarios_app:error_view')
    if request.method == 'POST' and request.is_ajax():
        data = []
        try:
            with transaction.atomic():
                # =====================  select ================
                action = request.POST['action']
                # id_user = request.user.id
                if action == 'buscardatos':
                    grupos = Group.objects.all()
                    for i in grupos:
                        grupo = {}
                        grupo["id"] = i.pk
                        grupo["name"] = i.name
                        data.append(grupo)
                # ======================== crear =========================
                elif action == 'crear':
                    #obtenemos datos de grupo y lista de permisos
                    nombre_grupo = request.POST['nombre']
                    permission = request.POST['permission_list']
                    permissions_list = permission.split(",")
                    # print(permissions_list)
                    #creamos el grupo
                    group = Group.objects.create(name=nombre_grupo)
                    #asignamos permisos al grupo
                    for permission_id in permissions_list:
                        # print('el id es: ',permission_id)
                        permission = Permission.objects.get(id=permission_id)
                        group.permissions.add(permission)
                    #guardamos cambios en la base de datos
                    group.save()

                    data = {'tipo_accion': 'crear', 'correcto': True}
                elif action == 'permisos_grupo':
                    grupo = Group.objects.get(pk= request.POST['id'])
                    #Esto obtiene los permisos que tiene el grupo asignados
                    permisos = grupo.permissions.all()
                    permisos_data = []
                    #aqui se guardan en la variable permisos_data
                    for permiso in permisos:
                        permiso_data = {}
                        permiso_data['name'] = permiso.name
                        permiso_data['id'] = permiso.pk
                        permisos_data.append(permiso_data)
                    # data.append(permisos_data)
                    # print(permisos_data)
                    response = JsonResponse(permisos_data, safe=False)
                    return response
                elif action == 'editar':
                    id_grupo = request.POST['id_grupo']
                    # Buscamos el grupo a editar
                    grupo = Group.objects.get(id=id_grupo)
                    #Esto obtiene los permisos modificados
                    permission = request.POST['permission_list']
                    permissions_list = permission.split(",")
                    # print(permissions_list)
                    
                    lista_permisos = [] #lista de permisos a setear
                    for permiso in permissions_list: #recorre la lista de permisos obtenida
                        permisos = Permission.objects.get(id=permiso) #buscamos el permiso y lo guardamos
                        # print(permisos.pk)
                        lista_permisos.append(permisos.pk) #agrega el id del permiso a la lista
                    grupo.permissions.set(lista_permisos) #cambia la lista de permisos del grupo por la lista nueva
                        
                    data = {'tipo_accion': 'editar', 'correcto': True}
                else:
                    data['error'] = 'Ha ocurrido un error.'
        except Exception as e:
            # print('error---> ',str(e))
            data['error'] = str(e)
            data = {'tipo_accion': 'error',  'correcto': False}
            transaction.rollback()
        else:
            transaction.commit()
        return JsonResponse(data, safe=False)
    elif request.method == 'GET':
        permisos = Permission.objects.all()
        grupos = Group.objects.all()
        return render(request, 'usuarios/grupos.html',{'permisos': permisos, 'grupos': grupos})

@login_required
def perfil_Usuarios(request):
    user = request.user.id
    usr = User.objects.get(pk=user)
    data_asignacion=[]
    data_tickets=[]
    empleado = Empleado.objects.get(usuario = usr)
    asignacion = historial_asignaciones.objects.filter(usuario = usr)
    
    nombre = empleado.usuario.first_name
    apellido = empleado.usuario.last_name
    email = empleado.usuario.email
    dni = empleado.dni
    depto = empleado.depto.nombre_depto

    for asg in asignacion:
        data_asg={}
        if asg.status == 'ASIGNADO':
            data_asg['correlativo'] = asg.inventario_item.correlativo
            data_asg['nombre_item'] = asg.inventario_item.nombre_item
            data_asg['serial'] = asg.inventario_item.serial_number
            data_asg['modelo'] = asg.inventario_item.ModeloItem.nombre_modelo
            data_asg['categoria'] = asg.inventario_item.categoria.nombre_categoria
            data_asg['imagen'] = asg.inventario_item.imagen_item
        data_asignacion.append(data_asg)

    return render(request, 'usuarios/profile.html',{
                    'asignaciones':data_asignacion,
                    'nombre':nombre,
                    'apellido':apellido,
                    'email':email,
                    'dni':dni,
                    'depto':depto,
                    })