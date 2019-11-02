from django.shortcuts import render

from .models import models

# Create your views here.

def home(request):
    return render(request, 'core/home.html')
