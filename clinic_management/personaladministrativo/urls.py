from django.urls import path
from . import views

urlpatterns = [
    path('home/personal_administrativo',views.crear_paciente,name='home_personal_administrativo'),
    path('home/personal_administrativo/crear_paciente',views.crear_paciente,name='crear_paciente')
]