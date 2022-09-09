from django.urls import path
from apps.asignaciones.views import *

app_name = 'asignaciones_app'

urlpatterns =[
    path('asignaciones/', asignacionViews, name='asignaciones')
]