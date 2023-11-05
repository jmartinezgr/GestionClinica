from django.urls import path
from . import views

urlpatterns = [
    path('home/medicos/crear_historia_clinica',views.crear_historia_clinica,name='crear_historia_clinica'),
]