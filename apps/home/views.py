from django.shortcuts import render
from django.views.generic import (
    TemplateView, CreateView,
    )
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class IndexHomeView(LoginRequiredMixin, TemplateView):
    template_name = "home/home.html"
    login_url = reverse_lazy('login_app:login')

