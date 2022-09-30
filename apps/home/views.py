from itertools import count
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from apps.tickets.models import Ticket, TicketStatus

from django.db.models import Count

# Create your views here.


#template_name = "home/home.html"

@login_required
def IndexHomeView(request):
    id_user = request.user.id
    estado_ticket = ['OPEN','IN_PROGRES','DONE']
    ticket_user = []
    for e in estado_ticket:
        est = {}
        est['estado'] = estado_ticket[e]
        est['cantidad'] = Ticket.objects.filter(user_id=id_user, status=estado_ticket[e]).count()
        ticket_user.append(est)
    ctx = {'estados':estado_ticket, 'ticket_user':ticket_user}
    return render(request, 'home/home.html',ctx)

def ticket_box(request):
    id_user = request.user.id
    estado_ticket = Ticket.objects.all()
    ticket_user = []
    for e in estado_ticket:
        if e.choices:
            est = {}
            est['estado'] = e.choices
            est['cantidad'] = Ticket.objects.filter(user_id=id_user, status=e.choices).count()
            ticket_user.append(est)
    ctx = {'estados':estado_ticket, 'ticket_user':ticket_user}
     

