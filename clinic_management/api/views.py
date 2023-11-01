# api/views.py
from rest_framework import generics
from personaladministrativo.models import Paciente
from .serializer import PacienteSerializer

class PacienteListCreateView(generics.ListCreateAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

class PacienteRetrieveView(generics.RetrieveAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    lookup_field = 'numero_identificacion'

class PacienteUpdateView(generics.UpdateAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    lookup_field = 'numero_identificacion'