from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from datetime import datetime
from django.utils import formats

from django.contrib.auth.models import User
from apps.inventario.models import *

from django.http import JsonResponse
# Create your views here.


@login_required
def inventarioViews(request):
    if request.method == 'POST' and request.is_ajax():
        data = []
        try:
            # =====================  select ================
            action = request.POST['action']
            id_user = request.user.id
            if action == 'buscardatos':
                for i in Inventario_Item.objects.all():
                    data.append(i.toJSON())
            # =====================  crear ================
            elif action == 'crear':

                inv = Inventario_Item()
                inv.correlativo = request.POST['correlativo']
                inv.nombre_item = request.POST['nombre_item']
                if int(request.POST['id_categoria']) > 0:
                    inv.categoria = Categoria.objects.get(pk=request.POST['id_categoria'])
                if int(request.POST['id_modelo']) > 0:
                    inv.ModeloItem = ModeloItem.objects.get(pk=request.POST['id_modelo'])
                if int(request.POST['id_proveedor']) > 0:
                    inv.proveedor = Proveedor.objects.get(pk=request.POST['id_proveedor'])
                inv.precio = request.POST['precio']
                inv.created_by = User.objects.get(pk=id_user)
                inv.fecha_compra = request.POST['fecha_compra']
                inv.fecha_garantia = request.POST['fecha_garantia']
                if int(request.POST['id_estado']) > 0:
                    inv.estado = Estado.objects.get(pk=request.POST['id_estado'])
                inv.caracteristica = request.POST['caracteristica']
                inv.comentarios = request.POST['comentarios']
                inv.serial_number = request.POST['serial_number']
                inv.ubicacion = request.POST['ubicacion']
                inv.save()

                if request.FILES:
                    imagen = request.FILES.get("imagen")
                    imagen.name = str(inv.pk)+" "+imagen.name
                    inv.imagen_item = imagen
                    inv.save()

                data = {'tipo_accion': 'crear', 'correcto': True}

            # =====================  editar  ================
            elif action == 'editar':
                updated_time = datetime.now()
                inv = Inventario_Item.objects.get(pk=request.POST['id'])
                inv.correlativo = request.POST['correlativo']
                inv.nombre_item = request.POST['nombre_item']
                if int(request.POST['id_categoria']) > 0:
                    inv.categoria = Categoria.objects.get(pk=request.POST['id_categoria'])
                if int(request.POST['id_modelo']) > 0:
                    inv.ModeloItem = ModeloItem.objects.get(pk=request.POST['id_modelo'])
                if int(request.POST['id_proveedor']) > 0:
                    inv.proveedor = Proveedor.objects.get(pk=request.POST['id_proveedor'])
                inv.precio = request.POST['precio']
                inv.updated_by = User.objects.get(pk=id_user)
                inv.fecha_compra = request.POST['fecha_compra']
                inv.fecha_garantia = request.POST['fecha_garantia']
                if int(request.POST['id_estado']) > 0:
                    inv.estado = Estado.objects.get(pk=request.POST['id_estado'])
                inv.caracteristica = request.POST['caracteristica']
                inv.comentarios = request.POST['comentarios']
                inv.serial_number = request.POST['serial_number']
                inv.ubicacion = request.POST['ubicacion']
                inv.updated_at = formats.date_format(updated_time)

                if request.FILES:
                    if inv.imagen_item.url != "/media/img_defecto.jpg":
                        inv.imagen_item.delete()
                    imagen = request.FILES.get("imagen")
                    imagen.name = str(inv.pk)+" "+imagen.name
                    inv.imagen_item = imagen
#validad que si el estado a actualizar es descarte que el equipo se descargo anteriormente estado == 2
                inv.save()
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
        categorias = Categoria.objects.all()
        modelos = ModeloItem.objects.all()
        proveedores = Proveedor.objects.all()
        estado = Estado.objects.all()
        return render(request, 'inventario/inventario_home.html', {'categorias': categorias, 'proveedores': proveedores, 
                        'modelos':modelos, 'estados':estado})


# =============================================================== Parametros ===========================================================================
@login_required
def categoriaViews(request):
    if request.method == 'POST' and request.is_ajax():
        data = []
        try:
            # =====================  select ================
            action = request.POST['action']
            id_user = request.user.id
            if action == 'buscardatos':
                for i in Categoria.objects.all():
                    data.append(i.toJSON())

            # ======================== crear =========================
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
        return render(request, 'inventario/categoria.html', {'titulo': 'Inicio', 'entidad': 'Creacion de categorias'})


@login_required
def marcasViews(request):
    if request.method == 'POST' and request.is_ajax():
        data = []
        try:
            # =====================  select ================
            action = request.POST['action']
            id_user = request.user.id
            if action == 'buscardatos':
                for i in Marca.objects.all():
                    data.append(i.toJSON())

            # ======================== crear =========================
            elif action == 'crear':
                ma = Marca()
                ma.nombre_marca = request.POST['nombre_marca']
                ma.created_by = User.objects.get(pk=id_user)
                ma.save()

                if request.FILES:
                    imagen = request.FILES.get("image")
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

                    imagen = request.FILES.get("image")
                    imagen.name = str(ma.pk)+" "+imagen.name
                    ma.image = imagen

                ma.save()

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
        return render(request, 'inventario/marcas.html', {'titulo': 'Inicio', 'entidad': 'Creacion de marcas'})


@login_required
def modeloViews(request):
    if request.method == 'POST' and request.is_ajax():
        data = []
        try:
            # =====================  select ================
            action = request.POST['action']
            id_user = request.user.id
            if action == 'buscardatos':
                for i in ModeloItem.objects.all():
                    data.append(i.toJSON())

            # ======================== crear =========================
            elif action == 'crear':
                mo = ModeloItem()
                mo.nombre_modelo = request.POST['nombre_modelo']
                mo.created_by = User.objects.get(pk=id_user)
                if int(request.POST['id_marca']) > 0:
                    mo.marca = Marca.objects.get(pk=request.POST['id_marca'])
                mo.save()

                data = {'tipo_accion': 'crear', 'correcto': True}
            elif action == 'editar':
                mo = ModeloItem.objects.get(pk=request.POST['id'])
                mo.nombre_modelo = request.POST['nombre_modelo']
                if int(request.POST['id_marca']) > 0:
                    mo.marca = Marca.objects.get(pk=request.POST['id_marca'])
                mo.save()

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
        marcas = Marca.objects.all()
        return render(request, 'inventario/modeloitem.html', {'marcas': marcas})

@login_required
def proveedoresViews(request):
    if request.method == 'POST' and request.is_ajax():
        data = []
        try:
            # =====================  select ================
            action = request.POST['action']
            id_user = request.user.id
            if action == 'buscardatos':
                for i in Proveedor.objects.all():
                    data.append(i.toJSON())

            # ======================== crear =========================
            elif action == 'crear':
                prov = Proveedor()
                prov.nombre_proveedor= request.POST['nombre_proveedor']
                prov.telefono = request.POST['telefono']
                prov.email = request.POST['email']
                prov.created_by = User.objects.get(pk=id_user)
                prov.save()

                data = {'tipo_accion': 'crear', 'correcto': True}
            elif action == 'editar':
                prov = Proveedor.objects.get(pk=request.POST['id'])
                prov.nombre_proveedor= request.POST['nombre_proveedor']
                prov.telefono = request.POST['telefono']
                prov.email = request.POST['email']
                prov.created_by = User.objects.get(pk=id_user)
                prov.save()

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
        return render(request, 'inventario/proveedores.html',{'titulo': 'Inicio', 'entidad':'Creacion de Proveedores'})

@login_required
def estadosViews(request):
    if request.method == 'POST' and request.is_ajax():
        data = []
        try:
            # =====================  select ================
            action = request.POST['action']
            id_user = request.user.id
            if action == 'buscardatos':
                for i in Estado.objects.all():
                    data.append(i.toJSON())

            # ======================== crear =========================
            elif action == 'crear':
                prov = Estado()
                prov.nombre_estado = request.POST['nombre_estado']
                prov.created_by = User.objects.get(pk=id_user)
                prov.save()

                data = {'tipo_accion': 'crear', 'correcto': True}
            elif action == 'editar':
                prov = Estado.objects.get(pk=request.POST['id'])
                prov.nombre_estado = request.POST['nombre_estado']
                prov.save()

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
        return render(request, 'inventario/estados.html',{'titulo': 'Inicio', 'entidad':'Creacion de Estados'})
# Parametros
