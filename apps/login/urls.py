from django.urls import path

from django.conf.urls import url

from apps.login.views import *


app_name = 'login_app'  #namespace

urlpatterns = [
    path('', login, name='login'),
    path('logout', logout_view, name='logout'),
]
