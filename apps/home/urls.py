from django.urls import path
from . import views

app_name = 'home_app' # namespace

urlpatterns = [
    path('home/', views.IndexHomeView.as_view(), name='home'),
]