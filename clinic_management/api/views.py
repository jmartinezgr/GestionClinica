from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from personaladministrativo.models import Paciente
from .serializer import PacienteSerializer
from rest_framework import status

@api_view(['GET'])
def paciente_list(request):
    pacientes = Paciente.objects.all()
    serializer = PacienteSerializer(pacientes, many=True)
    data = {
        'pacientes': serializer.data,
        'self': reverse('paciente-list', request=request),
    }
    return Response(data)

@api_view(['POST'])
def paciente_create(request):
    serializer = PacienteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def paciente_detail(request, numero_identificacion):
    try:
        paciente = Paciente.objects.get(numero_identificacion=numero_identificacion)
    except Paciente.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PacienteSerializer(paciente)
    data = {
        'paciente': serializer.data,
        'self': reverse('paciente-detail', args=[numero_identificacion], request=request),
        'update': reverse('paciente-update', args=[numero_identificacion], request=request),
        'partial_update': reverse('paciente-partial-update', args=[numero_identificacion], request=request),
        'delete': reverse('paciente-delete', args=[numero_identificacion], request=request),
    }
    return Response(data)

@api_view(['PUT'])
def paciente_update(request, numero_identificacion):
    try:
        paciente = Paciente.objects.get(numero_identificacion=numero_identificacion)
    except Paciente.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PacienteSerializer(paciente, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def paciente_partial_update(request, numero_identificacion):
    try:
        paciente = Paciente.objects.get(numero_identificacion=numero_identificacion)
    except Paciente.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PacienteSerializer(paciente, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def paciente_delete(request, numero_identificacion):
    try:
        paciente = Paciente.objects.get(numero_identificacion=numero_identificacion)
    except Paciente.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    paciente.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
