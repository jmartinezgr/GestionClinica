from django.urls import path
from . import views


urlpatterns = [
    path('home/recursos_humanos/',views.registro_view,name='home_recursos_humanos'),
    path('home/recursos_humanos/registro_pacientes/',views.registro_view,name='registro_usuarios'),
    path('home/recursos_humanos/buscar_usuario/',views.buscar_usuario, name= 'buscar_usuario'),
    path('home/recursos_humanos/editar_usuario/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('home/recursos_humanos/registrar_asistencia/', views.registrar_asistencia, name='registro_asistencia'),
]