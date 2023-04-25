from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.db import transaction
from apps.asignaciones.models import *
from apps.inventario.models import *
from apps.usuarios.models import *
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from weasyprint import HTML
from django.utils import timezone
# Create your views here.


@login_required
def PdfView(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.has_perm('asignaciones.view_historial_asignaciones')):
        return redirect('usuarios_app:error_view')
    if request.method == 'GET':
        try:
            id_asg = request.GET['asignacion_id']
            data_asignacion =  historial_asignaciones.objects.filter(id=id_asg)
            for asg in data_asignacion:
                data_asg = {}
                id = asg.pk
                status = asg.status
                fecha = asg.assigned_date.strftime('%Y-%m-%d')
                nombres = asg.usuario.first_name + ' ' + asg.usuario.last_name
                ident = Empleado.objects.get(usuario = asg.usuario)
                dni = ident.dni
                observaciones = asg.observaciones
                item = Inventario_Item.objects.get(id=asg.inventario_item.id)
                item_nombre = item.nombre_item
                item_caracteristica = item.caracteristica
                serie = item.serial_number
                modelo = item.ModeloItem.nombre_modelo
                marca = item.ModeloItem.marca.nombre_marca
            html_string = render_to_string('asignaciones/asignacion_pdf.html',{
                            'id':id,
                            'status':status,
                            'fecha':fecha,
                            'nombres':nombres,
                            'dni':dni,
                            'observaciones':observaciones,
                            'equipo':item_nombre,
                            'caracteristicas':item_caracteristica,
                            'serie':serie,
                            'modelo':modelo,
                            'marca':marca,
                            })
            html = HTML(string=html_string,base_url=request.build_absolute_uri()) #base url es lo que hace funcionar los archivos estaticos en el pdf
            response = HttpResponse(html.write_pdf(), content_type='application/pdf')
        except Exception as e: 
            print("Error: " + str(e))
        return response
    elif request.method =="POST":
        return None


@login_required
def asignacionViews(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.has_perm('asignaciones.view_historial_asignaciones')):
        return redirect('usuarios_app:error_view')
    if request.method == 'POST' and request.is_ajax():
        data = []
        try:
            #select
            with transaction.atomic():
                action = request.POST['action']
                id_user = request.user.id
                usuario_asg = User.objects.get(pk=id_user)
                updated_time = timezone.now()
                habBusqueda = request.POST['habBusqueda']
                if action == 'buscardatos':
                    if habBusqueda == 'false': 
                        for i in historial_asignaciones.objects.all().order_by('-id'):
                            data.append(i.toJSON())
                    elif habBusqueda == 'true':
                        busqueda = request.POST['busqueda']
                        busqueda_upper = busqueda.upper() 
                        try:
                            if (historial_asignaciones.objects.filter(usuario=User.objects.get(username=busqueda)).exists()):
                                for i in historial_asignaciones.objects.filter(usuario=User.objects.get(username=busqueda)).order_by('-id'):
                                    data.append(i.toJSON())
                        except User.DoesNotExist:
                            try:
                                if (historial_asignaciones.objects.filter(inventario_item=Inventario_Item.objects.get(correlativo=busqueda_upper)).exists()):
                                    for i in historial_asignaciones.objects.filter(inventario_item=Inventario_Item.objects.get(correlativo=busqueda_upper)).order_by('-id'):
                                        data.append(i.toJSON())
                            except Inventario_Item.DoesNotExist:
                                try:
                                    empleado = Empleado.objects.get(dni=busqueda)
                                    if (historial_asignaciones.objects.filter(usuario=User.objects.get(username=empleado.usuario)).exists()):
                                        for i in historial_asignaciones.objects.filter(usuario=User.objects.get(username=empleado.usuario)).order_by('-id'):
                                            data.append(i.toJSON())
                                except Empleado.DoesNotExist:
                                    for i in historial_asignaciones.objects.all().order_by('-id'):
                                        data.append(i.toJSON())
                #created
                elif action == 'crear':
                    equipo = request.POST['item_id']
                    inv = Inventario_Item.objects.get(pk=equipo)
                    #-------------------------------------
                    if inv.estado.id == 2:
                        asg = historial_asignaciones()
                        if int(request.POST['usuario_asignar'])>0:
                            asg.usuario = User.objects.get(pk=request.POST['usuario_asignar'])
                        if int(equipo)>0:
                            asg.inventario_item = Inventario_Item.objects.get(pk=equipo)
                        asg.status = 'ASIGNADO'
                        asg.assigned_by = usuario_asg
                        asg.update_by = usuario_asg
                        asg.observaciones = request.POST.get('observaciones')
                        asg.save()
                        #-------------------------------------
                        inv.estado = Estado.objects.get(pk=1)
                        inv.updated_at = updated_time
                        inv.save()
                        data = {'tipo_accion': 'crear', 'correcto': True}
                #editar
                elif action == 'descargo':
                    usuario_equipo = request.POST['usuario_asignar']
                    equipo = request.POST['item_id']
                    id_asignacion = request.POST['id_asignacion']
                    #-----------------Se crea el nuevo registro en el historial (No se actualiza ya que este necesita un historico)
                    historial_asignaciones.objects.filter(id=id_asignacion).create(
                        usuario = User.objects.get(pk=usuario_equipo),
                        inventario_item = Inventario_Item.objects.get(pk=equipo),
                        status = 'DESCARGO',
                        assigned_by = usuario_asg,
                        update_by = usuario_asg,
                        observaciones = request.POST.get('observaciones'),
                    )
                    #-----------Actualzia el equipo/item para que este disponible para proxima asignacion
                    Inventario_Item.objects.filter(id=equipo).update(
                        estado = 2,
                        updated_at = updated_time,
                    )

                    data = {'tipo_accion': 'descargo', 'correcto': True}
                # elif action == 'pdf':
                #     id_asg = request.POST['id_asignacion']
                    
                #     return redirect("asignaciones_app:nota", id_asg)
                    
                else:
                    data['error'] = 'Ha ocurrido un error.'
        except Exception as e:
            data['error'] = str(e)
            data = {'tipo_accion': 'error', 'correcto': True}
            transaction.rollback()
        else:
            transaction.commit()
        return JsonResponse(data, safe=False)
    elif request.method == 'GET': 
        invent = Inventario_Item.objects.all()
        usuarios = User.objects.all()
        return render(request, 'asignaciones/asignaciones.html', {'invent':invent, 'usuarios':usuarios})