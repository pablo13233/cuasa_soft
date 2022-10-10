from django.urls import path
from apps.asignaciones.views import *

app_name = 'asignaciones_app'

urlpatterns =[
    path('asignaciones/', asignacionViews, name='asignaciones'),
    path('pdf/', asignacion_pdf.as_view(), name='pdf'),
]