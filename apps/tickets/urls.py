from django.urls import path
from . import views

app_name = 'tickets_app' # namespace

urlpatterns = [
    path('ticket/', views.About, name='about'),
]