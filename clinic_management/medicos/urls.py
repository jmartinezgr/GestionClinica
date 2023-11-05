from django.urls import path
from . import views

urlpatterns = [
    path('home/medicos/',views.crear_historia_clinica,name='crear_historia_clinica'),
    path('home/medicos/crear_historia_clinica',views.crear_historia_clinica,name='crear_historia_clinica'),
    path('home/medicos/agregar_orden/',views.agregar_ordenes,name='agregar_ordenes'),
    path('home/medicos/agregar_orden/<int:id_historia_medica>/',views.agregar_ordenes_con_id,name='agregar_ordenes_con_id'),
    path('home/medicos/agregar_medicamento/<int:id_historia_medica>/', views.agregar_medicamento, name='agregar_medicamento'),
]