from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import formats, timezone
import datetime
from django.contrib.auth.models import User
from apps.inventario.models import *
from apps.asignaciones.models import historial_asignaciones
from django.db import transaction
from django.http import JsonResponse
from django.template.loader import render_to_string
from weasyprint import HTML


@login_required
def inventarioViews(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.has_perm('inventario.view_inventario_item')):
        return redirect('usuarios_app:error_view')
    if request.method == 'POST' and request.is_ajax():
        data = []
        try:
            with transaction.atomic():
            # =====================  select ================
                action = request.POST['action']
                id_user = request.user.id
                if action == 'buscardatos':
                    categoria_select = int(request.POST['categoria_select'])
                    if categoria_select == 0:
                        for i in Inventario_Item.objects.filter(estado_id__in=[1,2]):
                            data.append(i.toJSON())
                    elif categoria_select > 0:
                        for i in Inventario_Item.objects.filter(categoria=categoria_select,estado_id__in=[1,2]):
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
                    updated_time = timezone.now()
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
            # print(str(e))
            # print(action)
            data['error'] = str(e)
            data = {'tipo_accion': 'error',  'correcto': True}
            transaction.rollback()
        else:
            transaction.commit()
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
    if not (request.user.is_superuser or request.user.is_staff or request.user.has_perm('inventario.view_categoria')):
        return redirect('usuarios_app:error_view')
    if request.method == 'POST' and request.is_ajax():
        data = []
        try:
            with transaction.atomic():
            # =====================  select ================
                action = request.POST['action']
                id_user = request.user.id
                if action == 'buscardatos':
                    for i in Categoria.objects.all():
                        data.append(i.toJSON())
                    # print(data)
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
            # print(str(e))
            # print(action)
            data['error'] = str(e)
            data = {'tipo_accion': 'error',  'correcto': True}
            transaction.rollback()
        else:
            transaction.commit()
        return JsonResponse(data, safe=False)
    elif request.method == 'GET':
        return render(request, 'inventario/categoria.html', {'titulo': 'Inicio', 'entidad': 'Creacion de categorias'})


@login_required
def marcasViews(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.has_perm('inventario.view_marca')):
        return redirect('usuarios_app:error_view')
    if request.method == 'POST' and request.is_ajax():
        data = []
        try:
            with transaction.atomic():
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
            # print(str(e))
            # print(action)
            data['error'] = str(e)
            data = {'tipo_accion': 'error',  'correcto': True}
            transaction.rollback()
        else:
            transaction.commit()
        return JsonResponse(data, safe=False)
    elif request.method == 'GET':
        return render(request, 'inventario/marcas.html', {'titulo': 'Inicio', 'entidad': 'Creacion de marcas'})


@login_required
def modeloViews(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.has_perm('inventario.view_modeloitem')):
        return redirect('usuarios_app:error_view')
    if request.method == 'POST' and request.is_ajax():
        data = []
        try:
            with transaction.atomic():
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
            # print(str(e))
            # print(action)
            data['error'] = str(e)
            data = {'tipo_accion': 'error',  'correcto': True}
            transaction.rollback()
        else:
            transaction.commit()
        return JsonResponse(data, safe=False)
    elif request.method == 'GET':
        marcas = Marca.objects.all()
        return render(request, 'inventario/modeloitem.html', {'marcas': marcas})

@login_required
def proveedoresViews(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.has_perm('inventario.view_proveedor')):
        return redirect('usuarios_app:error_view')
    if request.method == 'POST' and request.is_ajax():
        data = []
        try:
            with transaction.atomic():
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
            # print(str(e))
            # print(action)
            data['error'] = str(e)
            data = {'tipo_accion': 'error',  'correcto': True}
            transaction.rollback()
        else:
            transaction.commit()
        return JsonResponse(data, safe=False)
    elif request.method == 'GET':
        return render(request, 'inventario/proveedores.html',{'titulo': 'Inicio', 'entidad':'Creacion de Proveedores'})

@login_required
def estadosViews(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.has_perm('inventario.view_estado')):
        return redirect('usuarios_app:error_view')
    if request.method == 'POST' and request.is_ajax():
        data = []
        try:
            with transaction.atomic():
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
            # print(str(e))
            # print(action)
            data['error'] = str(e)
            data = {'tipo_accion': 'error',  'correcto': True}
            transaction.rollback()
        else:
            transaction.commit()
        return JsonResponse(data, safe=False)
    elif request.method == 'GET':
        return render(request, 'inventario/estados.html',{'titulo': 'Inicio', 'entidad':'Creacion de Estados'})
# Parametros

@login_required
def descarteViews(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.has_perm('inventario.delete_inventario_item')):
        return redirect('usuarios_app:error_view')
    if request.method == 'POST' and request.is_ajax():
        data = []
        try:
            with transaction.atomic():
                # =====================  select ================
                action = request.POST['action']
                id_user = request.user.id
                if action == 'buscardatos':
                    if request.POST['fecha_ini'] == None or request.POST['fecha_final'] == None:
                        for i in Inventario_Item.objects.filter(estado_id=3):
                            data.append(i.toJSON())
                    else:
                        fecha_ini = timezone.make_aware(datetime.datetime.strptime(request.POST['fecha_ini'],'%Y-%m-%d')) 
                        fecha_final = timezone.make_aware(datetime.datetime.strptime(request.POST['fecha_final'], '%Y-%m-%d'))
                        for i in Inventario_Item.objects.filter(estado_id=3, updated_at__range=[fecha_ini, fecha_final]):
                            data.append(i.toJSON())
                
                # ======================== crear =========================
                elif action == 'crear':
                    Inventario_Item.objects.filter(pk=request.POST['item_id']).update(
                        comentarios=request.POST['comentario'],
                        estado_id=3,
                        updated_at = timezone.now(),
                        updated_by = User.objects.get(pk=id_user),
                    )

                    data = {'tipo_accion': 'crear', 'correcto': True}
                elif action == 'editar':
                    prov = Estado.objects.get(pk=request.POST['id'])
                    prov.nombre_estado = request.POST['nombre_estado']
                    prov.save()

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
        invent = Inventario_Item.objects.filter(estado_id=2)
        return render(request, 'inventario/descarte.html',{'invent':invent})

#--------------- PDF

@login_required
def pdfInventarioView(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.has_perm('inventario.delete_inventario_item')):
        return redirect('usuarios_app:error_view')
    if request.method == 'GET':
        try:
            id_item = request.GET['item']
            data_item =  Inventario_Item.objects.filter(id=id_item)
            for itm in data_item:
                nombre = itm.nombre_item
                correlativo = itm.correlativo
                caracteristica = itm.caracteristica
                comentarios = itm.comentarios
                fecha_descarte = itm.updated_at
                usuario_desscarta = itm.updated_by.username
                serie = itm.serial_number
                modelo = itm.ModeloItem.nombre_modelo
                marca = itm.ModeloItem.marca.nombre_marca
                categoria = itm.categoria.nombre_categoria
            html_string = render_to_string('inventario/descarte_pdf.html',{
                            'id_item':id_item,
                            'nombre':nombre,
                            'correlativo':correlativo,
                            'caracteristica':caracteristica,
                            'comentarios':comentarios,
                            'fecha_descarte':fecha_descarte,
                            'serie':serie,
                            'modelo':modelo,
                            'marca':marca,
                            'usuario_desscarta':usuario_desscarta,
                            'categoria':categoria,
                            })
            html = HTML(string=html_string,base_url=request.build_absolute_uri()) #base url es lo que hace funcionar los archivos estaticos en el pdf
            response = HttpResponse(html.write_pdf(), content_type='application/pdf')
        except Exception as e: 
            print("Error: " + str(e))
        return response
    elif request.method =="POST":
        return None
    
@login_required
def mantenimientosViews(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.has_perm('inventario.add_historico_mantenimientos')):
        return redirect('usuarios_app:error_view')
    if request.method == 'POST' and request.is_ajax():
        data = []
        try:
            with transaction.atomic():
                # =====================  select ================
                action = request.POST['action']
                id_user = request.user.id
                if action == 'buscardatos':
                    if request.POST['fecha_ini'] == None or request.POST['fecha_final'] == None:
                        print('Error en fechas')
                    else:
                        fecha_ini = timezone.make_aware(datetime.datetime.strptime(request.POST['fecha_ini'],'%Y-%m-%d')) 
                        fecha_final = timezone.make_aware(datetime.datetime.strptime(request.POST['fecha_final'], '%Y-%m-%d'))
                        for i in historico_mantenimientos.objects.filter(updated_at__range=[fecha_ini, fecha_final]):
                            data.append(i.toJSON())
                
                # ======================== crear =========================
                elif action == 'crear':
                    if (request.POST['cambio_partes'] == 'false'):
                            n_cambio_parte = False
                    elif (request.POST['cambio_partes'] == 'true'):
                        n_cambio_parte = True
                    
                    hm = historico_mantenimientos()
                    hm.inventario_item = Inventario_Item.objects.get(id=request.POST['item_id'])
                    hm.title = request.POST['title']
                    hm.cambio_partes = n_cambio_parte
                    hm.comentario = request.POST['comentario']
                    hm.updated_at = timezone.now()
                    hm.created_by = User.objects.get(pk=id_user)
                    hm.updated_by = User.objects.get(pk=id_user)
                    hm.save()
                    if request.FILES:
                        imagen = request.FILES.get("imagen")
                        imagen.name = str(hm.pk)+" "+imagen.name
                        hm.imagen_mantenimiento = imagen
                        hm.save()

                    data = {'tipo_accion': 'crear', 'correcto': True}
                elif action == 'editar':
                    prov = Estado.objects.get(pk=request.POST['id'])
                    prov.nombre_estado = request.POST['nombre_estado']
                    prov.save()

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
        invent = Inventario_Item.objects.filter(estado_id__in=[1,2])
        return render(request, 'inventario/mantenimiento.html',{'invent':invent})

@login_required
def pdfMantenimientoView(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.has_perm('inventario.add_historico_mantenimientos')):
        return redirect('usuarios_app:error_view')
    if request.method == 'GET':
        try:
            id_mtn = request.GET['id']
            data_mtn =  historico_mantenimientos.objects.filter(id=id_mtn)
            for mtn in data_mtn:
                title = mtn.title
                correlativo = mtn.inventario_item.correlativo
                item = Inventario_Item.objects.get(correlativo=mtn.inventario_item.correlativo)
                comentarios = mtn.comentario
                serie = mtn.inventario_item.serial_number
                caracteristicas = mtn.inventario_item.caracteristica
                fecha_crea = mtn.created_at
                usuario_creo = mtn.created_by.username
                cambio_partes = mtn.cambio_partes
            try:
                data_asg = historial_asignaciones.objects.get(inventario_item = item)
                for asg in data_asg:
                    asignado = asg.usuario.username
            except historial_asignaciones.DoesNotExist:
                asignado = 'No asignado'
            html_string = render_to_string('inventario/mantenimiento_pdf.html',{
                            'correlativo':correlativo,
                            'title':title,
                            'fecha_crea':fecha_crea,
                            'comentarios':comentarios,
                            'usuario_creo':usuario_creo,
                            'cambio_partes':cambio_partes,
                            'serie':serie,
                            'asignado':asignado,
                            'caracteristicas':caracteristicas,
                            })
            html = HTML(string=html_string,base_url=request.build_absolute_uri()) #base url es lo que hace funcionar los archivos estaticos en el pdf
            response = HttpResponse(html.write_pdf(), content_type='application/pdf')
        except Exception as e: 
            print("Error: " + str(e))
        return response
    elif request.method =="POST":
        return None