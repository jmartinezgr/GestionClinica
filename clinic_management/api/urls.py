# api/urls.py
from django.urls import path
from .views import PacienteListCreateView

urlpatterns = [
    path('pacientes/', PacienteListCreateView.as_view(), name='paciente-list-create'),
    # Agrega otras URL para actualizar, eliminar, obtener detalles, etc.
]
