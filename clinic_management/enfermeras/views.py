from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Visitas
from personaladministrativo.models  import Paciente
from .forms import InformacionAdicionalForm
import datetime
from django.contrib import messages
from decorators.custom_decorators import role_required

@role_required(['Enfermeras','Soporte de Información'])
def visitas_pendientes(request):
    # Obtener todas las visitas con estado False y ordenar por hora de creación (más antigua primero)
    visitas_pendientes = Visitas.objects.filter(estado=False).order_by('fecha')
    context = {
        'visitas_pendientes': visitas_pendientes,
    }

    return render(request, 'visitas_pendientes.html', context)

@role_required(['Enfermeras','Soporte de Información'])
def detalle_visita(request, visita_id):
    # Obtener la visita específica
    visita = Visitas.objects.get(id=visita_id)

    if request.method == 'POST':
        form = InformacionAdicionalForm(request.POST, instance=visita)
        if form.is_valid():
            # Guardar la información adicional en la visita
            form.save()

            # Cambiar el estado de la visita a True
            visita.estado = True
            visita.fecha_realizacion = datetime.datetime.now()
            visita.save()

            historia = visita.orden_hospitalizacion

            if historia.agregar_visita():
                nueva_visita = Visitas(
                    paciente = visita.paciente,
                    orden_hospitalizacion = visita.orden_hospitalizacion
                )

                nueva_visita.save()

            # Redireccionar a la página de visitas pendientes
            return redirect('visitas_pendientes')
    else:
        form = InformacionAdicionalForm(instance=visita)

    context = {
        'visita': visita,
        'form': form,
    }

    return render(request, 'detalle_visita.html', context)

@role_required(['Enfermeras','Soporte de Información'])
def buscar_visitas(request):
    if request.method == 'POST':
        numero_identificacion = request.POST.get('numero_identificacion')
        try:
            paciente = Paciente.objects.get(numero_identificacion=numero_identificacion)
        except Paciente.DoesNotExist:
            messages.error(request, "No se ha encontrado un paciente con esa cedula")
            return redirect('buscar_visitas')
        
        try:
            visita = Visitas.objects.get(paciente=paciente,estado=False)
            return redirect('detalle_visita', visita.id)
        except Visitas.DoesNotExist:
            messages.error(request, "No se encontraron visitas asignadas a este paciente")
            return redirect('buscar_visitas')

    return render(request, 'busqueda_visita.html')