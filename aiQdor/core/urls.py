from django.urls import path

# o '.' server para importar algo do mesmo diretorio
from . import views

urlpatterns = [
    path('', views.home, name="core-home")
]
