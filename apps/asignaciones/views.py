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
            if action == 'buscardatos': 
                for i in historial_asignaciones.objects.all().order_by('-id'):
                    data.append(i.toJSON())
            #created
            elif action == 'crear':
                control_act=[]
                for i in control_Asignaciones.objects.filter(usuario=request.POST['usr_control']):
                    control_act.append(i.toJSON())
                


                data = {'tipo_accion': 'crear', 'corrector': True}
            #editar
            elif action == 'editar':    
                data = {'tipo_accion': 'editar', 'corrector': True}
            else:
                data['error'] = 'Ha ocurrido un error.'
        except Exception as e:
            print(str(e))
            print(action)
            data['error'] = str(e)
            data = {'tipo_accion': 'error', 'corrector': True}
        return JsonResponse(data, safe=False)
    elif request.method == 'GET': 
        invent = Inventario_Item.objects.all()
        usuarios = User.objects.all()
        return render(request, 'asignaciones/asignaciones.html', {'invent':invent, 'usuarios':usuarios})