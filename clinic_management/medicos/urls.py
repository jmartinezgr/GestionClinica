from django.urls import path
from . import views

urlpatterns = [
    path('home/medicos/',views.crear_historia_clinica,name='crear_historia_clinica'),
    path('home/medicos/crear_historia_clinica',views.crear_historia_clinica,name='crear_historia_clinica'),
    path('home/medicos/agregar_orden/',views.agregar_ordenes,name='agregar_ordenes'),
    path('home/medicos/agregar_orden/<int:id_historia_medica>/',views.agregar_ordenes_con_id,name='agregar_ordenes_con_id'),
    path('home/medicos/agregar_medicamento/<int:id_historia_medica>/', views.agregar_medicamento, name='agregar_medicamento'),
    path('home/medicos/agregar_procedimiento/<int:id_historia_medica>/', views.agregar_procedimiento, name='agregar_procedimiento'),
    path('home/medicos/agregar_ayuda_diagnostica/<int:id_historia_medica>/', views.agregar_ayuda_diagnostica, name='agregar_ayuda_diagnostica'),
]