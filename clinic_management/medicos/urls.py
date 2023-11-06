from django.urls import path
from . import views

urlpatterns = [
    path('home/medicos/', views.crear_historia_clinica, name='home_medicos'),
    path('home/medicos/crear_historia_clinica', views.crear_historia_clinica, name='crear_historia_clinica'),
    path('home/medicos/agregar_orden/', views.agregar_ordenes, name='agregar_ordenes'),
    path('home/medicos/agregar_orden/<int:id_historia_medica>/', views.agregar_ordenes_con_id, name='agregar_ordenes_con_id'),
    path('home/medicos/agregar_medicamento/<int:id_historia_medica>/', views.agregar_medicamento, name='agregar_medicamento'),
    path('home/medicos/agregar_procedimiento/<int:id_historia_medica>/', views.agregar_procedimiento, name='agregar_procedimiento'),
    path('home/medicos/agregar_ayuda_diagnostica/<int:id_historia_medica>/', views.agregar_ayuda_diagnostica, name='agregar_ayuda_diagnostica'),
    path('home/medicos/agregar_hospitalizacion/<int:id_historia_medica>/',views.agregar_hospitalizacion,name="agregar_hospitalizacion"),
    path('home/medicos/estado_historia/', views.buscar_estado_historia, name='buscar_estado_historia'),
    path('home/medicos/estado_historia/<int:id_historia_medica>/', views.estado_historia, name='estado_historia'),
    path('home/medicos/cerrar_orden/<int:id_orden>/', views.cerrar_orden, name='cerrar_orden'),
    path('home/medicos/cerrar_ayuda_diagnostica/<int:id_orden>/', views.cerrar_ayuda_diagnostica, name='cerrar_ayuda_diagnostica'),
    path('home/medicos/cerrar_historia_medica/<int:id_historia_medica>/', views.cerrar_historia_clinica, name='cerrar_historia_clinica'),
]