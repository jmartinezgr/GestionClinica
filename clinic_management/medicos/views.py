from django.shortcuts import render, redirect
from .forms import HistoriaClinicaForm, OrdenMedicamentoForm
from user.models import Usuario
from personaladministrativo.models import Paciente
from .models import HistoriaClinica

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
    return render(request, 'elegir_orden_con_id.html', {'id_historia_medica': id_historia_medica})

def agregar_medicamento(request, id_historia_medica):
    #historia_clinica = HistoriaClinica.objects.get(id=id_historia_medica)

    if request.method == 'POST':
        form = OrdenMedicamentoForm(request.POST)
        if form.is_valid():
            orden_medicamento = form.save(commit=False)
            orden_medicamento.orden = 1 #historia_clinica
            orden_medicamento.save()
            return redirect('agregar_ordenes', id_historia_medica=id_historia_medica)

    else:
        form = OrdenMedicamentoForm()

    return render(request, 'agregar_medicamento.html', {'form': form})
