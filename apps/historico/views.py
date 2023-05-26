from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse, HttpResponse
#
import datetime
from django.utils import timezone
from datetime import datetime, timedelta
#
from apps.historico.models import *
# Create your views here.

@login_required
def historicoView (request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.has_perm('historico.view_historico')):
        return redirect('usuarios_app:error_view')
    if request.method == 'POST' and request.is_ajax():
        
        try:
            data = []
            with transaction.atomic():
                #========================   select   =========================
                action = request.POST['action']
                
                if action == 'buscardatos':
                    if request.POST['fecha_ini'] == '' or request.POST['fecha_final'] == '':
                        hoy = timezone.now() 
                        fecha_hoy = hoy.replace(hour=23, minute=59, second=59, microsecond=999)
                        fecha_inicio = hoy - timedelta(days=30)
                        for i in historico.objects.filter(created_at__range=[fecha_inicio, fecha_hoy]):
                            data.append(i.toJSON())
                    else:
                        fecha_ini = timezone.make_aware(datetime.strptime(request.POST['fecha_ini'],'%Y-%m-%d')) 
                        fecha_final_1 = timezone.make_aware(datetime.strptime(request.POST['fecha_final'], '%Y-%m-%d'))
                        fecha_final = fecha_final_1.replace(hour=23, minute=59, second=59, microsecond=999)
                        print(fecha_ini)
                        print(fecha_final)
                        for i in historico.objects.filter(created_at__range=[fecha_ini, fecha_final]):
                            data.append(i.toJSON())

                    # data = {'tipo_accion': 'buscardatos', 'correcto': True}
        except Exception as e:
            data['error'] = str(e)
            print("Error--->",e)
            data = {'tipo_accion': 'error','correcto': False, 'error': str(e)}
            transaction.rollback()
        else:
            transaction.commit()
        return JsonResponse(data,safe=False)
    elif request.method =="GET":
        return render(request, 'historico/historial.html')