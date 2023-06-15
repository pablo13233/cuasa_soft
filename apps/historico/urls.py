from django.urls import path
from apps.historico.views import *

app_name = 'historico_app' # namespace

urlpatterns = [
    path('historial',historicoView, name='historial'),
]