from django.urls import path
from apps.tickets.views import *

app_name = 'tickets_app' # namespace

urlpatterns = [
    path('ticket/', ticketViews, name='ticket_view'),
    path('admin-ticket/', AdminTicketViews, name='admin_ticket'),
    path('categorias-ticket', categoria_ticket_view, name='categorias_ticket'),
]