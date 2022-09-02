from django.urls import path
from apps.tickets.views import *

app_name = 'tickets_app' # namespace

urlpatterns = [
    path('ticket/', ticketViews, name='ticket_view'),
    path('admin-ticket/', AdminTicketViews, name='admin_ticket'),
]