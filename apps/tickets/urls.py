from django.urls import path
from apps.tickets.views import *

app_name = 'tickets_app' # namespace

urlpatterns = [
    path('ticket/', ticketViews, name='ticket_view'),
    path('ticket/admin-ticket/<id>/', AdminTicketViews, name='admin_ticket'),
    path('ticket/categorias-ticket', categoria_ticket_view, name='categorias_ticket'),
    path('ticket/comentarios/', commentTicket_view, name='comentarios'),
    path('reportes/ticket/', ticket_categorias_view, name='reporte_categoria'), #eliminar
    path('reportes/ticket-categoria', ticket_categorias_pdf, name='ticket_categoria'),
    path('reportes/', reportes_views, name='reportes'),
    path('reportes/incidencia-departamento', ticket_departamento_pdf, name='incidencia_departamento'),
    path('reportes/categoria-departamento', categoria_departamento_pdf, name='categoria_departamento'),
    path('reportes/ticket-categoria-prueba', ticket_departamento_test, name='ticket_categoria-prueba'),
]