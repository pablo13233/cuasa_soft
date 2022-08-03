from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required

from apps.usuarios.models import User
from apps.inventario.models import *
 
from django.http import JsonResponse
# Create your views here.

@login_required
def inventarioViews (request):
    if request.method == 'POST' and request.is_ajax():
        data=[]
        try:
            #=====================  select ================
            action = request.POST['action']
            id_user = request.user.id
            if action == 'buscardatos':
                for i in Inventario_Item.objects.all():
                    data.append(i.toJSON())
            #=====================  crear ================
            elif action == 'crear':
                
                data = {'tipo_accion':'crear', 'correcto': True}

            #=====================  editar  ================
            elif action == 'editar':
                 
                data = {'tipo_accion': 'editar', 'correcto':True}

            #=====================  baja  ================
            elif action == 'baja': 

                data = {'tipo_accion': 'baja', 'correcto':True}
            else:
                data['error'] = 'Ha ocurrido un error.'
        except Exception as e:
            data['error'] = str(e)
            data = {'tipo_accion': 'error',  'correcto': True}
    elif request.method == 'GET':
        return render(request, 'inventario/inventario_home.html', {'titulo':'Inicio', 'entidad':'Creacion de Items para inventario'})


# =============================================================== Parametros ===========================================================================
@login_required
def categoriaViews (request):
    if request.method == 'POST' and request.is_ajax():
        data=[]
        try:
            #=====================  select ================
            action = request.POST['action']
            id_user = request.user.id
            if action == 'buscardatos':
                for i in Categoria.objects.all():
                    data.append(i.toJSON())

            #======================== crear =========================
            elif action == 'crear':
                ca = Categoria()
                ca.nombre_categoria = request.POST['nombre_categoria']
                ca.created_by = User.objects.get(pk=id_user)
                ca.save()
            
                data = {'tipo_accion': 'crear', 'correcto': True}
            elif action == 'editar': 
                ca = Categoria.objects.get(pk=request.POST['id'])
                ca.nombre_categoria = request.POST['nombre_categoria']
                ca.save()

                data = {'tipo_accion': 'editar', 'correcto':True}
            else:
                data['error'] = 'Ha ocurrido un error.'
        except Exception as e:
            print(str(e))
            print(action)
            data['error'] = str(e)
            data = {'tipo_accion': 'error',  'correcto': True}
        return JsonResponse(data, safe=False)
    elif request.method == 'GET':
        return render(request, 'inventario/categoria.html', {'titulo':'Inicio', 'entidad':'Creacion de categorias'})


@login_required
def marcasViews (request):
    if request.method == 'POST' and request.is_ajax():
        data=[]
        try:
            #=====================  select ================
            action = request.POST['action']
            id_user = request.user.id
            if action == 'buscardatos':
                for i in Marca.objects.all():
                    data.append(i.toJSON())

            #======================== crear =========================
            elif action == 'crear':
                ma = Marca()
                ma.nombre_marca = request.POST['nombre_marca']
                ma.created_by = User.objects.get(pk=id_user)
                ma.save()

                if request.FILES:
                    imagen = request.FILES.get('image')
                    imagen.name = str(ma.pk)+" "+imagen.name
                    ma.image = imagen
                    ma.save()
                data = {'tipo_accion': 'crear', 'correcto': True}
            elif action == 'editar': 
                ma = Marca.objects.get(pk=request.POST['id'])
                ma.nombre_marca = request.POST['nombre_marca']

                if request.FILES:
                    if ma.image.url != "/media/img_defecto.jpg":
                        ma.image.delete()
                    
                    imagen = request.FILES.get('image')
                    imagen.name = str(ma.pk)+" "+imagen.name
                    ma.image = imagen

                ma.save()

                data = {'tipo_accion': 'editar', 'correcto':True}
            else:
                data['error'] = 'Ha ocurrido un error.'
        except Exception as e:
            print(str(e))
            print(action)
            data['error'] = str(e)
            data = {'tipo_accion': 'error',  'correcto': True}
        return JsonResponse(data, safe=False)
    elif request.method == 'GET':
        return render(request, 'inventario/marcas.html', {'titulo':'Inicio', 'entidad':'Creacion de marcas'})


# Parametros