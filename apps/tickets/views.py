from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required

from apps.usuarios.models import User
from apps.tickets.models import Ticket
 
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
            if action =='buscardatos':
                for i in Ticket.objects.filter(user_id = id_user):
                    data.append(i.toJSON())

                    #========================   Crear   =========================
            elif action =='crear':

                dato_Ticket = Ticket()
                dato_Ticket.title = request.POST['title']
                dato_Ticket.description = request.POST['description']

                dato_Ticket.user_id = User.objects.get(pk=id_user)
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
        return render(request, 'tickets/ticket_home.html')


@login_required
def AdminTicketViews (request):
    if request.method == 'POST' and request.is_ajax():
        data = []
        try:
            #========================   select Tickets Abiertos  =========================
            action = request.POST['action']

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
                print(request.POST['id'])
                dato_Ticket = Ticket.objects.get(pk=request.POST['id'])
                
                dato_Ticket.status = "IN_PROGRESS"

                if int(request.POST['assignee_id'])>0:
                    dato_Ticket.assignee_id = User.objects.get(pk=request.POST['assignee_id'])
                

                dato_Ticket.save()
                data = {'tipo_accion': 'actualizarOpen', 'correcto': True}

            
        except Exception as e: 
            data['error'] = str(e)
            data = {'tipo_accion': 'error','correcto': False, 'error': str(e)}

        return JsonResponse(data,safe=False)
    elif request.method =="GET":
        users = User.objects.filter(is_staff=True)
        return render(request, 'tickets/ticket_admin.html',{'users':users})