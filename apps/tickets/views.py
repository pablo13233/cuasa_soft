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
            if action =='buscardatos':
                for i in Ticket.objects.all():
                    data.append(i.toJSON())

                    #========================   Crear   =========================
            elif action =='crear':

                dato_Ticket = Ticket()
                dato_Ticket.title = request.POST['title']
                dato_Ticket.description = request.POST['description']

                dato_Ticket.user_id = User.objects.get(pk=request.user.id)
                dato_Ticket.save()

                if request.FILES:
                    imagen = request.FILES.get("imagen")
                    imagen.name = str(dato_Ticket.pk)+"_"+imagen.name
                    dato_Ticket.img_ticket = imagen
                    dato_Ticket.save()#Actualizamos la ruta de la imagen con la concatenacion del id recien creado
                data = {'tipo_accion': 'crear', 'correcto': True}

                #========================   editar   =========================
            elif action == 'editar':

                dato_Ticket = Ticket.objects.get(pk=request.POST['id'])
                dato_Ticket.title = request.POST['title']
                dato_Ticket.status = request.POST['status']
                dato_Ticket.description = request.POST['description']

                if request.FILES:
                    if dato_Ticket.img_ticket.url != "/media/img_defecto.jpg":
                        dato_Ticket.img_ticket.delete()

                    imagen = request.FILES.get("imagen")
                    imagen.name = str(dato_Ticket.pk)+"_"+imagen.name
                    dato_Ticket.img_ticket = imagen
                    
                dato_Ticket.save()
                data = {'tipo_accion': 'editar', 'correcto': True}

                #========================   eliminar   =========================
            elif action =='eliminar':
                dato_Ticket = Ticket.objects.get(pk=request.POST['id'])
                if dato_Ticket.img_ticket.url != "/media/img_defecto.jpg":
                    dato_Ticket.img_ticket.delete()

                dato_Ticket.delete()
                data = {'tipo_accion': 'eliminar','correcto': True}
            else:
                data['error'] = 'Ha ocurrido un error'
            
        except Exception as e:
            data['error'] = str(e)
            data = {'tipo_accion': 'error','correcto': False, 'error': str(e)}
        return JsonResponse(data,safe=False)
    elif request.method =="GET":
        return render(request, 'tickets/ticket_home.html')