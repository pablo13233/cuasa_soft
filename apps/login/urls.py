from django.urls import path
from . import views

from django.conf.urls import url
from rest_framework.authtoken import views

app_name = 'login_app'  # namespace

urlpatterns = [
    url(r'^login/', views.Login.as_view(), name='login'),
    url(r'^logout/', views.Logout.as_view(), name='logout'), 
]
