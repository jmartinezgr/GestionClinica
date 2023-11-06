from django.urls import path
from . import views

urlpatterns = [
    path('home/enfermeras/visitas_pendientes/', views.visitas_pendientes, name='visitas_pendientes'),
    path('home/enfermeras/buscar_visitas/',views.buscar_visitas,name='buscar_visitas'),
    path('home/enfermeras/detalle_visita/<int:visita_id>/', views.detalle_visita, name='detalle_visita'),
]
