from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from datetime import datetime
from django.utils import formats
from django.http import JsonResponse

from apps.asignaciones.models import *
from apps.inventario.models import *
from apps.usuarios.models import *
# Create your views here.
@login_required
def asignacionViews(request):
    if request.method == 'POST' and request.is_ajax():
        data = []
        try:
            #select
            action = request.POST['action']
            id_user = request.user_id
            updated_time = datetime.now()
            equipo = request.POST['item_id']
            inv = Inventario_Item.objects.get(pk=equipo)
            if action == 'buscardatos': 
                for i in historial_asignaciones.objects.all().order_by('-id'):
                    data.append(i.toJSON())
            #created
            elif (action == 'crear') and (inv.status == 2):
                
                asg = historial_asignaciones()
                if int(request.POST['usuario_asignar']>0):
                    asg.usuario = User.objects.get(pk=request.POST['usuario_asignar'])
                if int(request.POST['item_id']>0):
                    asg.inventario_item = Inventario_Item.objects.get(pk=equipo)
                asg.assigned_by = User.objects.get(pk=id_user)
                asg.update_by = User.objects.get(pk=id_user)
                asg.observaciones = request.POST.get('observaciones')
                asg.save()
                #-------------------------------------
                inv.status = 1
                inv.updated_at = updated_time
                inv.save()

                data = {'tipo_accion': 'crear', 'correcto': True}
            #editar
            elif action == 'editar':
                
                inv.status = 1
                inv.updated_at = updated_time
                inv.save()
                #-------------------------------------
                asg = historial_asignaciones.objects.get()
                asg.estado = 'DESCARGO'
                asg.updated_date = updated_time
                asg.updated_by = User.objects.get(pk=id_user)
                asg.save()

                data = {'tipo_accion': 'editar', 'correcto': True}
            else:
                data['error'] = 'Ha ocurrido un error.'
        except Exception as e:
            print(str(e))
            print(action)
            data['error'] = str(e)
            data = {'tipo_accion': 'error', 'correcto': True}
        return JsonResponse(data, safe=False)
    elif request.method == 'GET': 
        invent = Inventario_Item.objects.all()
        usuarios = User.objects.all()
        return render(request, 'asignaciones/asignaciones.html', {'invent':invent, 'usuarios':usuarios})