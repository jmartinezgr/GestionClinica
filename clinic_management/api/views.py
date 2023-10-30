# api/views.py
from rest_framework import generics
from personaladministrativo.models import Paciente
from .serializer import PacienteSerializer

class PacienteListCreateView(generics.ListCreateAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
