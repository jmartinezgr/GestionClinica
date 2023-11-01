from django.urls import path
from .views import PacienteListCreateView, PacienteRetrieveView, PacienteUpdateView

urlpatterns = [
    path('pacientes/', PacienteListCreateView.as_view(), name='paciente-list-create'),
    path('pacientes/<str:numero_identificacion>/', PacienteRetrieveView.as_view(), name='paciente-retrieve'),
    path('pacientes/<str:numero_identificacion>/update/', PacienteUpdateView.as_view(), name='paciente-update'),
]
