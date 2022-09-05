from itertools import count
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from apps.tickets.models import Ticket

from django.db.models import Count

# Create your views here.


#template_name = "home/home.html"

@login_required
def IndexHomeView(request):
    return render(request, 'home/home.html')

def ticket_chart(request):
    labels = []
    data = []

    queryset = Ticket.objects.values('status').annotate(ticket_count=Count('status'))
    for entry in queryset:
        labels.append(entry['status'])
        data.append(entry['ticket_count'])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
