from django.utils import formats
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from apps.tickets.models import *
from django.db.models import Q
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone
import datetime
# Create your views here.

@login_required
def ticketViews (request):
    if request.method == 'POST' and request.is_ajax():
        
        try:
            data = []
            with transaction.atomic():
                #========================   select   =========================
                action = request.POST['action']
                id_user = request.user.id
                query = Q(status="OPEN")
                query.add(Q(status="IN_PROGRESS"),Q.OR)
                query.add(Q(user_id=id_user),Q.AND)

                if action =='buscardatos':
                    for i in Ticket.objects.filter(query):
                        data.append(i.toJSON())
                        print(i.created_at)
                        #========================   Crear   =========================
                elif action =='crear':

                    dato_Ticket = Ticket()
                    if int(request.POST['categoria'])>0:
                        dato_Ticket.categoria = categoria_ticket.objects.get(pk=request.POST['categoria'])
                    dato_Ticket.title = request.POST['title']
                    dato_Ticket.description = request.POST['description']

                    dato_Ticket.user_id = User.objects.get(pk=id_user)
                    dato_Ticket.updated_by = User.objects.get(pk=id_user)
                    dato_Ticket.save()

                    if request.FILES:
                        imagen = request.FILES.get("imagen")
                        imagen.name = str(dato_Ticket.pk)+"_"+imagen.name
                        dato_Ticket.img_ticket = imagen
                        dato_Ticket.save()#Actualizamos la ruta de la imagen con la concatenacion del id recien creado
                    data = {'tipo_accion': 'crear', 'correcto': True}
        except Exception as e:
            data['error'] = str(e)
            print("Error--->",e)
            data = {'tipo_accion': 'error','correcto': False, 'error': str(e)}
            transaction.rollback()
        else:
            transaction.commit()
        return JsonResponse(data,safe=False)
    elif request.method =="GET":
        categoria = categoria_ticket.objects.all()
        return render(request, 'tickets/ticket_home.html',{'categorias': categoria})


@login_required
def AdminTicketViews (request,id):
    if not (request.user.is_superuser or request.user.is_staff or request.user.has_perm('tickets.delete_ticket')):
        return redirect('usuarios_app:error_view')
    if request.method == 'POST' and request.is_ajax():
        data = []
        try:
            with transaction.atomic():
                estado = 'NADA'
                if int(id) == 1:
                    estado = 'OPEN'
                elif int(id) == 2:
                    estado = 'IN_PROGRESS'
                elif int(id) == 3:
                    estado = 'DONE'
                #========================   select Tickets Abiertos  =========================
                action = request.POST['action']
                id_user = request.user.id
                date_up = timezone.now()
                if action =='buscardatos':
                    if estado == 'OPEN' or estado == 'IN_PROGRESS':
                        for i in Ticket.objects.filter(status=estado):
                            data.append(i.toJSON())
                    elif estado == 'DONE':
                        fecha_ini = timezone.make_aware(datetime.datetime.strptime(request.POST['fecha_ini'],'%Y-%m-%d')) 
                        fecha_final = timezone.make_aware(datetime.datetime.strptime(request.POST['fecha_final'], '%Y-%m-%d'))
                        for i in Ticket.objects.filter(status=estado, created_at__range=[fecha_ini, fecha_final]):
                            data.append(i.toJSON())
                        #========================   Crear   =========================
                elif action =='actualizarOpen':
                    dato_Ticket = Ticket.objects.get(pk=request.POST['id'])
                    
                    dato_Ticket.status = "IN_PROGRESS"
                    dato_Ticket.updated_by = User.objects.get(pk=id_user)
                    dato_Ticket.updated_at = formats.date_format(date_up)

                    if int(request.POST['assignee_id'])>0:
                        dato_Ticket.assignee_id = User.objects.get(pk=request.POST['assignee_id'])
                        dato_Ticket.save()
                        data = {'tipo_accion': 'actualizarOpen', 'correcto': True}

                elif action =='actualizarProgress':
                    dato_Ticket = Ticket.objects.get(pk=request.POST['id'])
                    dato_Ticket.status = "DONE"
                    dato_Ticket.updated_by = User.objects.get(pk=id_user)
                    dato_Ticket.updated_at = formats.date_format(date_up)

                    dato_Ticket.save()
                    data = {'tipo_accion': 'actualizarProgress', 'correcto': True}
        except Exception as e: 
            data['error'] = str(e)
            data = {'tipo_accion': 'error','correcto': False, 'error': str(e)}
            transaction.rollback()
        else:
            transaction.commit()
        return JsonResponse(data,safe=False)
    elif request.method =="GET":
        users = User.objects.filter(is_staff=True)
        return render(request, 'tickets/ticket_admin.html',{'users':users})

@login_required
def categoria_ticket_view(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.has_perm('tickets.view_categoria_ticket')):
        return redirect('usuarios_app:error_view')
    if request.method == 'POST' and request.is_ajax():
        data =[]
        try:
            with transaction.atomic():
                action = request.POST['action']
                id_user = request.user.id
                date_up = timezone.now()

                if action == 'buscardatos':
                    for i in categoria_ticket.objects.all():
                        data.append(i.toJSON())

                elif action == 'crear':
                    ca = categoria_ticket()
                    ca.tittle = request.POST['tittle']
                    ca.description = request.POST['description']
                    ca.created_by = User.objects.get(pk=id_user)
                    ca.updated_by = User.objects.get(pk=id_user)
                    ca.save()

                    data = {'tipo_accion':'crear', 'correcto':True}
                elif action == 'editar':
                    ca = categoria_ticket.objects.get(pk=request.POST['id'])
                    ca.tittle = request.POST['tittle']
                    ca.description = request.POST['description']
                    ca.updated_by = User.objects.get(pk=id_user)
                    ca.updated_at = formats.date_format(date_up)
                    ca.save()

                    data = {'tipo_accion':'editar', 'correcto':True}
                else:
                    data['error'] = 'Ha ocurrido un error.'
        except Exception as e:
            # print(str(e))
            data['error'] = str(e)
            data = {'tipo_accion':'error', 'correcto':True}
            transaction.rollback()
        else:
            transaction.commit()
        return JsonResponse(data, safe=False)
    elif request.method =="GET":
        return render(request, 'tickets/categorias.html')


@login_required
def commentTicket_view(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.has_perm('commentTicket.view_comentticket')):
        return redirect('usuarios_app:error_view')
    if request.method =="GET":
        id_t = request.GET['id_ticket']
        return render(request, 'tickets/comentarios.html',{'ticket':id_t})
    elif request.method == 'POST' and request.is_ajax():
        data =[]
        try:
            with transaction.atomic():
                action = request.POST['action']
                id_user = request.user.id
                date_up = timezone.now()
                id_t = int(request.POST['ticket'])
                if action == 'buscardatos':
                    for i in commentTicket.objects.filter(id_ticket = id_t):
                        data.append(i.toJSON())
                elif action == 'crear':
                    # print('lol ',id_t)
                    commentTicket.objects.create(
                        id_ticket=Ticket.objects.get(pk=id_t),
                        title = request.POST['title'],
                        comment = request.POST['comments'],
                        created_by = User.objects.get(pk=id_user),
                        updated_by = User.objects.get(pk=id_user),
                    )

                    data = {'tipo_accion':'crear', 'correcto':True}
                elif action == 'editar':
                    commentTicket.objects.filter(pk=request.POST['id_comment']).update(
                        title = request.POST['title'],
                        comment = request.POST['comments'],
                        updated_by = User.objects.get(pk=id_user),
                        updated_at = date_up
                    )

                    data = {'tipo_accion':'editar', 'correcto':True}
                else:
                    data['error'] = 'Ha ocurrido un error.'
        except Exception as e:
            # print(str(e))
            data['error'] = str(e)
            data = {'tipo_accion':'error', 'correcto':True}
            transaction.rollback()
        else:
            transaction.commit()
        return JsonResponse(data, safe=False)