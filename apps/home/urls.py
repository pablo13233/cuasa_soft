from django.urls import path
from apps.home.views import *

app_name = 'home_app' # namespace

urlpatterns = [
    path('home/', IndexHomeView, name='home'),
]