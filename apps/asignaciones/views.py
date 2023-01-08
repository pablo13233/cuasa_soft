from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import JsonResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO

from django.views.generic import View
from django.db import transaction
from apps.asignaciones.models import *
from apps.inventario.models import *
from django.contrib.auth.models import User
# Create your views here.

# html a pdf
def html_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type="application/pdf")
    return None
#

class asignacion_pdf(View):
    def get(self, request, *args, **kwargs):
        pdf= html_to_pdf('asignaciones/asignacion_pdf.html')
        return HttpResponse(pdf, content_type="application/pdf")


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
                updated_time = datetime.now()
                if action == 'buscardatos': 
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
                        asg.assigned_by = User.objects.get(pk=id_user)
                        asg.update_by = User.objects.get(pk=id_user)
                        asg.observaciones = request.POST.get('observaciones')
                        asg.save()
                        #-------------------------------------
                        inv.estado = Estado.objects.get(pk=1)
                        inv.updated_at = updated_time
                        inv.save()
                        data = {'tipo_accion': 'crear', 'correcto': True}
                #editar
                elif action == 'editar':
                    equipoe = request.POST['equipo_ver']
                    inve = Inventario_Item.objects.get(correlativo=equipoe)
                    #-------------------------------------
                    asg = historial_asignaciones()
                    if int(request.POST['usuario_asignar']>0):
                        asg.usuario = User.objects.get(username=request.POST['usuario_ver'])
                    if int(request.POST['equipo_ver']>0):
                        asg.inventario_item = Inventario_Item.objects.get(correlativo=equipo)
                    asg.status = 'DESCARGO'
                    asg.update_by = User.objects.get(pk=id_user)
                    asg.observaciones = request.POST.get('observaciones')
                    asg.save()
                    #-------------------------------------
                    inve.estado = 2
                    inve.updated_at = updated_time
                    inve.save()

                    data = {'tipo_accion': 'editar', 'correcto': True}
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