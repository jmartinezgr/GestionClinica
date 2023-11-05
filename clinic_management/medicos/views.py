from django.shortcuts import render, redirect
from .forms import HistoriaClinicaForm, OrdenMedicamentoForm, OrdenProcedimientoForm
from user.models import Usuario
from personaladministrativo.models import Paciente
from .models import *

def crear_historia_clinica(request):
    if request.method == 'POST':
        form = HistoriaClinicaForm(request.POST)
        if form.is_valid():
        
            try:
                medico = Usuario.objects.get(cedula=form.cleaned_data['medico'])
            except:
                print('Medico no encontrado')
                return redirect('crear_historia_clinica')
            
            try:
                paciente = Paciente.objects.get(numero_identificacion=form.cleaned_data['paciente'])
            except:
                print('No encontro el paciente')
                return redirect('crear_historia_clinica')
            
            try:
                historia_clinica_verificacion = HistoriaClinica.objects.get(paciente=paciente,cerrada=False)
                print("Aun hay una historia clinica activa")
                return redirect('agregar_ordenes_con_id', id_historia_medica=historia_clinica_verificacion.id)
            except:
                pass
 
            if medico.rol.name == 'Médicos' :
           
                historia_clinica = HistoriaClinica(
                    medico=medico,
                    paciente=paciente,
                    motivo_consulta=form.cleaned_data['motivo_consulta'],
                    sintomatologia=form.cleaned_data['sintomatologia'],
                    diagnostico=form.cleaned_data['diagnostico'],
                    fecha = form.cleaned_data['fecha']
                )
                historia_clinica.save()
                
                # Redirige a la vista "agregar_ordenes" pasando la ID de la historia médica
                return redirect('agregar_ordenes_con_id', id_historia_medica=historia_clinica.id)
            else:
                return redirect('crear_historia_clinica')
        
        else:
            print('Formulario no valido')
            print(form.errors)
    else:
        form = HistoriaClinicaForm()

    return render(request, 'crear_historia.html', {'form': form})

def agregar_ordenes(request):
    
    if request.method == 'POST':
        numero_identificacion = request.POST.get('numero_identificacion')
        try:
            paciente = Paciente.objects.get(numero_identificacion=numero_identificacion)
        except:
            return redirect('agregar_ordenes')
        
        try:
            historia_clinica = HistoriaClinica.objects.get(paciente=paciente,cerrada=False)
        except:
            return redirect('agregar_ordenes')
        
        return redirect('agregar_ordenes_con_id',historia_clinica.id)
    
    return render(request,'elegir_orden.html')

def agregar_ordenes_con_id(request, id_historia_medica):
    
    try:
        historia_clinica = HistoriaClinica.objects.get(id=id_historia_medica,cerrada=False)
    except:
        return redirect('agregar_ordenes')
    
    return render(request, 'elegir_orden_con_id.html', {'id_historia_medica': id_historia_medica})

def agregar_medicamento(request, id_historia_medica):
    historia_clinica = HistoriaClinica.objects.get(id=id_historia_medica)
    
    # Verifica si existe una orden de Ayuda Diagnóstica sin cerrar
    if historia_clinica.ordenes.filter(tipo_orden='ayuda_diagnostica', cerrada=False).exists():
        # Si existe una orden de Ayuda Diagnóstica sin cerrar, no se permite crear una orden de medicamento
        return redirect('agregar_ordenes', id_historia_medica=id_historia_medica)
    
    if request.method == 'POST':
        form = OrdenMedicamentoForm(request.POST)
        if form.is_valid():
            # Busca el número de ítem máximo en las órdenes de medicamento de la historia clínica actual
            max_item = historia_clinica.ordenes.filter(
                tipo_orden='medicamento',
                medicamentos__isnull=False,
            ).aggregate(models.Max('medicamentos__numero_item'))['medicamentos__numero_item__max']
            
            # Asigna el nuevo número de ítem
            numero_item = max_item + 1 if max_item is not None else 1

            nueva_orden = Orden(
                    paciente=historia_clinica.paciente,
                    medico=historia_clinica.medico,
                    tipo_orden='medicamento',  # Tipo de orden Medicamento
            )

            nueva_orden.save()

            # Crea una nueva orden de medicamento
            orden_medicamento = OrdenMedicamento(
                orden=nueva_orden,
                numero_item=numero_item,
                nombre_medicamento=form.cleaned_data['nombre_medicamento'],
                dosis=form.cleaned_data['dosis'],
                duracion_tratamiento=form.cleaned_data['duracion_tratamiento'],
                costo=form.cleaned_data['costo'],
            )
            orden_medicamento.save()

            # Agrega la nueva orden de medicamento a la historia clínica
            historia_clinica.ordenes.add(orden_medicamento.orden)

            return redirect('agregar_ordenes_con_id', id_historia_medica=id_historia_medica)
    else:
        form = OrdenMedicamentoForm()

    return render(request, 'agregar_medicamento.html', {'form': form})

def agregar_procedimiento(request, id_historia_medica):
    historia_clinica = HistoriaClinica.objects.get(id=id_historia_medica)

    if request.method == 'POST':
        form = OrdenProcedimientoForm(request.POST)
        if form.is_valid():
            # Crear una nueva orden
            nueva_orden = Orden(
                paciente=historia_clinica.paciente,
                medico=historia_clinica.medico,
                tipo_orden='procedimiento',  # Tipo de orden Procedimiento
            )
            nueva_orden.save()

            max_item = historia_clinica.ordenes.filter(
                tipo_orden='procedimiento',
                medicamentos__isnull=False,
            ).aggregate(models.Max('medicamentos__numero_item'))['medicamentos__numero_item__max']
            
            # Asigna el nuevo número de ítem
            numero_item = max_item + 1 if max_item is not None else 1

            # Crear una nueva orden de procedimiento
            orden_procedimiento = OrdenProcedimiento(
                orden=nueva_orden,
                numero_item=numero_item,  # Asignar el número de ítem apropiado
                nombre_procedimiento=form.cleaned_data['nombre_procedimiento'],
                numero_veces=form.cleaned_data['numero_veces'],
                frecuencia=form.cleaned_data['frecuencia'],
                costo=form.cleaned_data['costo'],
                requiere_asistencia_especialista=form.cleaned_data['requiere_asistencia_especialista'],
            )
            orden_procedimiento.save()

            # Agregar la nueva orden de procedimiento a la historia clínica
            historia_clinica.ordenes.add(nueva_orden)

            return redirect('agregar_ordenes_con_id', id_historia_clinica=id_historia_medica)
    else:
        form = OrdenProcedimientoForm()

    return render(request, 'agregar_procedimiento.html', {'form': form})