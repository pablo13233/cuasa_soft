from django.urls import path
from apps.tickets.views import *

app_name = 'tickets_app' # namespace

urlpatterns = [
    path('ticket/', ticketViews, name='ticket_view'),
    path('ticket/admin-ticket/<id>/', AdminTicketViews, name='admin_ticket'),
    path('ticket/categorias-ticket', categoria_ticket_view, name='categorias_ticket'),
    path('ticket/comentarios/', commentTicket_view, name='comentarios')
]