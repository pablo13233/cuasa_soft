from django.shortcuts import render
from django.views.generic import (
    TemplateView, CreateView,
    )
from django.urls import reverse_lazy

# Create your views here.

class IndexHomeView(TemplateView):
    template_name = "home/home.html"

