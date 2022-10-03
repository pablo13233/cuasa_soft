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
    ticket_1 = 0
    ticket_2 = 0
    ticket_3 = 0

    cnt_1 = Ticket.objects.filter(user_id=id_user, status="OPEN").count()
    if cnt_1 > 0:
        ticket_1 = cnt_1
    else:
        ticket_1 = 0

    cnt_2 = Ticket.objects.filter(user_id=id_user, status="IN_PROGRESS").count()
    if cnt_2 > 0:
        ticket_2 = cnt_2
    else:
        ticket_2 = 0

    cnt_3 = Ticket.objects.filter(user_id=id_user, status="DONE").count()
    if cnt_3 > 0:
        ticket_3 = cnt_3
    else:
        ticket_3 = 0

    ctx = {'ticket_abiertos': ticket_1,'ticket_progreso': ticket_2,'ticket_cerrado': ticket_3}
    return render(request, 'home/home.html',ctx)

     

