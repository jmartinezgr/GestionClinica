from django.shortcuts import render, redirect
from .forms import HistoriaClinicaForm, OrdenMedicamentoForm, OrdenProcedimientoForm, OrdenAyudaDiagnosticaForm, OrdenAyudaDiagnosticaFinalForm
from user.models import Usuario
from personaladministrativo.models import Paciente
from .models import *
from django.contrib import messages

def crear_historia_clinica(request):
    if request.method == 'POST':
        form = HistoriaClinicaForm(request.POST)
        if form.is_valid():
        
            try:
                medico = Usuario.objects.get(cedula=form.cleaned_data['medico'])
            except:
                messages.error(request,"No se ha encontrado un medico con este numero de cedula")
                return redirect('crear_historia_clinica')
            
            try:
                paciente = Paciente.objects.get(numero_identificacion=form.cleaned_data['paciente'])
            except:
                messages.error(request,"No se ha encontrado un paciente con este numero de cedula")
                return redirect('crear_historia_clinica')
            
            try:
                historia_clinica_verificacion = HistoriaClinica.objects.get(paciente=paciente,cerrada=False)
                messages.error(request,"Ya existe una historia clinica activa")
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
                messages.error(request,"La cedula no pertenece a la de un medico")
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
            messages.error(request,"No hay ningun paciente con un ")            
            return redirect('agregar_ordenes')
        
        try:
            historia_clinica = HistoriaClinica.objects.get(paciente=paciente,cerrada=False)
        except:
            messages.error(request,"No se ha encontrado una historia medica donde agregar el proceso")            
            return redirect('agregar_ordenes')
        
        return redirect('agregar_ordenes_con_id',historia_clinica.id)
    
    return render(request,'elegir_orden.html')

def agregar_ordenes_con_id(request, id_historia_medica):
    
    try:
        historia_clinica = HistoriaClinica.objects.get(id=id_historia_medica,cerrada=False)
    except:
        messages.error(request,"No se ha encontrado una historia clinica con este numero de cedula")
        return redirect('agregar_ordenes')
    
    return render(request, 'elegir_orden_con_id.html', {'id_historia_medica': id_historia_medica})

def agregar_medicamento(request, id_historia_medica):
    historia_clinica = HistoriaClinica.objects.get(id=id_historia_medica)
    
    # Verifica si existe una orden de Ayuda Diagnóstica sin cerrar
    if historia_clinica.ordenes.filter(tipo_orden='ayuda_diagnostica', cerrada=False).exists():
        # Si existe una orden de Ayuda Diagnóstica sin cerrar, no se permite crear una orden de medicamento
        messages.error(request,"No puedes agregar un medicamento sin obtener los resultados de los examenes")
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

    # Verifica si existe una orden de Ayuda Diagnóstica sin cerrar
    if historia_clinica.ordenes.filter(tipo_orden='ayuda_diagnostica', cerrada=False).exists():
        # Si existe una orden de Ayuda Diagnóstica sin cerrar, no se permite crear una orden de medicamento
        messages.error(request,"No puedes agregar un procedimiento sin obtener los resultados de los examenes")
        return redirect('agregar_ordenes', id_historia_medica=id_historia_medica)

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

def agregar_ayuda_diagnostica(request, id_historia_medica):
    historia_clinica = HistoriaClinica.objects.get(id=id_historia_medica)

    if request.method == 'POST':
        form = OrdenAyudaDiagnosticaForm(request.POST)
        if form.is_valid():
            # Crear una nueva orden de ayuda diagnóstica
            nueva_orden = Orden(
                paciente=historia_clinica.paciente,
                medico=historia_clinica.medico,
                tipo_orden='ayuda_diagnostica',  # Tipo de orden Ayuda Diagnóstica
            )
            nueva_orden.save()

            # Crear una nueva orden de ayuda diagnóstica
            orden_ayuda_diagnostica = OrdenAyudaDiagnostica(
                orden=nueva_orden,
                nombre_ayuda_diagnostica=form.cleaned_data['nombre_ayuda_diagnostica'],
                cantidad=form.cleaned_data['cantidad'],
                costo=form.cleaned_data['costo'],
                requiere_asistencia_especialista=form.cleaned_data['requiere_asistencia_especialista'],
            )
            orden_ayuda_diagnostica.save()

            # Agregar la nueva orden de ayuda diagnóstica a la historia clínica
            historia_clinica.ordenes.add(nueva_orden)

            return redirect('agregar_ordenes_con_id', id_historia_medica=id_historia_medica)
    else:
        form = OrdenAyudaDiagnosticaForm()

    return render(request, 'agregar_ayuda_diagnostica.html', {'form': form})

def buscar_estado_historia(request):
        
    if request.method == 'POST':
        numero_identificacion = request.POST.get('numero_identificacion')
        try:
            paciente = Paciente.objects.get(numero_identificacion=numero_identificacion)
        except:
            messages.error(request,"No existe un paciente con ese numero de cedula")
            return redirect('agregar_ordenes')
        
        try:
            historia_clinica = HistoriaClinica.objects.get(paciente=paciente,cerrada=False)
        except:
            messages.error(request,"No existe una historia clinica para este numero de cedula")            
            return redirect('agregar_ordenes')
        
        return redirect('estado_historia',historia_clinica.id)
    
    return render(request,'elegir_orden_historia.html')


def estado_historia(request, id_historia_medica):
    historia_clinica = HistoriaClinica.objects.get(id=id_historia_medica)
    paciente_nombre = historia_clinica.paciente.nombre_completo

    # Filtrar órdenes de diferentes tipos
    ordenes_medicamentos = historia_clinica.ordenes.filter(tipo_orden='medicamento', cerrada=False)
    ordenes_procedimientos = historia_clinica.ordenes.filter(tipo_orden='procedimiento', cerrada=False)
    ordenes_ayuda_diagnostica = historia_clinica.ordenes.filter(tipo_orden='ayuda_diagnostica', cerrada=False)

    # Recopilamos información detallada de las órdenes de medicamentos
    detalles_ordenes_medicamentos = []
    for orden in ordenes_medicamentos:
        orden_medicamento = OrdenMedicamento.objects.get(orden=orden)
        detalle = {
            'id': orden.id,
            'nombre_medicamento': orden_medicamento.nombre_medicamento,
            'dosis': orden_medicamento.dosis,
            'duracion_tratamiento': orden_medicamento.duracion_tratamiento,
        }
        detalles_ordenes_medicamentos.append(detalle)

    # Recopilamos información detallada de las órdenes de procedimientos
    detalles_ordenes_procedimientos = []
    for orden in ordenes_procedimientos:
        orden_procedimiento = OrdenProcedimiento.objects.get(orden=orden)
        detalle = {
            'id': orden.id,
            'nombre_procedimiento': orden_procedimiento.nombre_procedimiento,
            'numero_veces': orden_procedimiento.numero_veces,
            'frecuencia': orden_procedimiento.frecuencia,
        }
        detalles_ordenes_procedimientos.append(detalle)

    # Recopilamos información detallada de las órdenes de ayuda diagnóstica
    detalles_ordenes_ayuda_diagnostica = []
    for orden in ordenes_ayuda_diagnostica:
        orden_ayuda_diagnostica = OrdenAyudaDiagnostica.objects.get(orden=orden)
        detalle = {
            'id': orden.id,
            'nombre_ayuda_diagnostica': orden_ayuda_diagnostica.nombre_ayuda_diagnostica,
            'cantidad': orden_ayuda_diagnostica.cantidad,
            'requiere_asistencia_especialista': orden_ayuda_diagnostica.requiere_asistencia_especialista,
        }
        detalles_ordenes_ayuda_diagnostica.append(detalle)

    return render(request, 'estado_historia_clinica.html', {
        'historia_clinica': historia_clinica,
        'paciente_nombre': paciente_nombre,
        'detalles_ordenes_medicamentos': detalles_ordenes_medicamentos,
        'detalles_ordenes_procedimientos': detalles_ordenes_procedimientos,
        'detalles_ordenes_ayuda_diagnostica': detalles_ordenes_ayuda_diagnostica,
    })

def cerrar_orden(request, id_orden):
    orden = Orden.objects.get(id=id_orden)

    if orden.tipo_orden == 'medicamento':
        # Cerrar orden de medicamento
        medicamento = OrdenMedicamento.objects.get(orden=orden)
        medicamento.cerrada = True
        medicamento.save()
    elif orden.tipo_orden == 'procedimiento':
        # Cerrar orden de procedimiento
        procedimiento = OrdenProcedimiento.objects.get(orden=orden)
        procedimiento.cerrada = True
        procedimiento.save()
    elif orden.tipo_orden == 'ayuda_diagnostica':
        # Redirigir a la vista para cerrar Ayuda Diagnóstica
        return redirect('cerrar_ayuda_diagnostica', id_orden=id_orden)

    # Marcar la orden principal como cerrada
    orden.cerrada = True
    orden.save()

    # Redirigir a la página de estado de la historia clínica
    messages.success(request,"Se cerro la orden con exito")
    return redirect('estado_historia', id_historia_medica=orden.historias_clinicas.first().id)

def cerrar_ayuda_diagnostica(request, id_orden):
    orden_ayuda_diagnostica = OrdenAyudaDiagnostica.objects.get(orden_id=id_orden)

    if request.method == 'POST':
        form = OrdenAyudaDiagnosticaFinalForm(request.POST, instance=orden_ayuda_diagnostica)
        if form.is_valid():
            form.save()

            orden = Orden.objects.get(id=id_orden)

            orden.cerrada = True
            orden.save()

            # Marcar la orden de Ayuda Diagnóstica como cerrada
            orden_ayuda_diagnostica.cerrada = True
            orden_ayuda_diagnostica.save()
            
            # Redirigir a la página de estado de la historia clínica
            messages.success(request,"Se cerro la ayuda diagnostica con exito")
            return redirect('estado_historia', id_historia_medica=orden_ayuda_diagnostica.orden.historias_clinicas.first().id)
    else:
        form = OrdenAyudaDiagnosticaFinalForm(instance=orden_ayuda_diagnostica)

    return render(request, 'cerrar_ayuda_diagnostica.html', {'form': form, 'orden_id': id_orden})

def cerrar_historia_clinica(request, id_historia_medica):

    historia = HistoriaClinica.objects.get(id=id_historia_medica)

    historia.cerrada = True
    historia.save()

    messages.success(request,"Se cerro la historia clinica con exito")
    return redirect('crear_historia_clinica')