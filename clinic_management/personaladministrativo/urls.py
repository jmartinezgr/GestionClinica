from django.urls import path
from . import views

urlpatterns = [
    path('home/personal_administrativo',views.crear_paciente,name='home_personal_administrativo'),
    path('home/personal_administrativo/crear_paciente',views.crear_paciente,name='crear_paciente'),
    path('home/personal_administrativo/buscar_paciente',views.buscar_paciente,name='buscar_paciente'),
    path('home/personal_administrativo/actualizar_paciente/<str:numero_identificacion>/',views.actualizar_paciente,name='actualizar_paciente')
]