"""
from django.urls import path
from .views import PacienteListCreateView, PacienteRetrieveView, PacienteUpdateView

urlpatterns = [
    path('pacientes/', PacienteListCreateView.as_view(), name='paciente-list-create'),
    path('pacientes/<str:numero_identificacion>/', PacienteRetrieveView.as_view(), name='paciente-retrieve'),
    path('pacientes/<str:numero_identificacion>/update/', PacienteUpdateView.as_view(), name='paciente-update'),
]"""

from django.urls import path
from .views import paciente_list, paciente_create, paciente_detail, paciente_update, paciente_partial_update, paciente_delete

urlpatterns = [
    path('pacientes/', paciente_list, name='paciente-list'),
    path('pacientes/create/', paciente_create, name='paciente-create'),
    path('pacientes/<str:numero_identificacion>/', paciente_detail, name='paciente-detail'),
    path('pacientes/<str:numero_identificacion>/update/', paciente_update, name='paciente-update'),
    path('pacientes/<str:numero_identificacion>/partial-update/', paciente_partial_update, name='paciente-partial-update'),
    path('pacientes/<str:numero_identificacion>/delete/', paciente_delete, name='paciente-delete'),
]
