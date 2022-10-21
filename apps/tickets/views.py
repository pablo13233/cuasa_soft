from datetime import datetime
from django.utils import formats
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.auth.models import User
from apps.tickets.models import *
from django.db.models import Q
 
from django.http import JsonResponse
# Create your views here.

@login_required
def ticketViews (request):
    if request.method == 'POST' and request.is_ajax():
        data = []

        try:
            #========================   select   =========================
            action = request.POST['action']
            id_user = request.user.id
            query = Q(status="OPEN")
            query.add(Q(status="IN_PROGRESS"),Q.OR)
            query.add(Q(user_id=id_user),Q.AND)

            if action =='buscardatos':
                for i in Ticket.objects.filter(query):
                    data.append(i.toJSON())
  
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
            data = {'tipo_accion': 'error','correcto': False, 'error': str(e)}
        return JsonResponse(data,safe=False)
    elif request.method =="GET":
        categoria = categoria_ticket.objects.all()
        return render(request, 'tickets/ticket_home.html',{'categorias': categoria})


@login_required
def AdminTicketViews (request):
    if request.method == 'POST' and request.is_ajax():
        data = []
        try:
            #========================   select Tickets Abiertos  =========================
            action = request.POST['action']
            id_user = request.user.id
            date_up = datetime.now()

            if action =='ticketsopen':
                for i in Ticket.objects.filter(status='OPEN'):
                    data.append(i.toJSON())

            #========================   select Tickets Progreso  =========================
            elif action =='ticketsprogress':
                for i in Ticket.objects.filter(status='IN_PROGRESS'):
                    data.append(i.toJSON())

            #========================   select Tickets Terminados  =========================
            elif action =='ticketdone':
                for i in Ticket.objects.filter(status='DONE'):
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

        return JsonResponse(data,safe=False)
    elif request.method =="GET":
        users = User.objects.filter(is_staff=True)
        return render(request, 'tickets/ticket_admin.html',{'users':users})

@login_required
def categoria_ticket_view(request):
    if request.method == 'POST' and request.is_ajax():
        data =[]
        try:
            action = request.POST['action']
            id_user = request.user.id
            date_up = datetime.now()

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
            print(str(e))
            data['error'] = str(e)
            data = {'tipo_accion':'error', 'correcto':True}
        return JsonResponse(data, safe=False)
    elif request.method =="GET":
        return render(request, 'tickets/categorias.html')