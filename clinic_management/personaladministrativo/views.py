from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
import requests
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from .models import Paciente
from medicos.models import *
from .forms import PacienteForm


@login_required
def home_personal_administrativo(request):
    return render(request, 'personaladministrativo.html', {'user': request.user})

@login_required
def crear_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            # Recopila los datos del formulario
            fecha_nacimiento = form.cleaned_data['fecha_nacimiento'].strftime("%Y-%m-%d")  # Formatea la fecha
            data = {
                "numero_identificacion": form.cleaned_data['numero_identificacion'],
                "nombre_completo": form.cleaned_data['nombre_completo'],
                "fecha_nacimiento": fecha_nacimiento,
                "genero": form.cleaned_data['genero'],
                "direccion": form.cleaned_data['direccion'],
                "numero_telefono": form.cleaned_data['numero_telefono'],
                "correo_electronico": form.cleaned_data['correo_electronico'],
                "nombre_contacto_emergencia": form.cleaned_data['nombre_contacto_emergencia'],
                "relacion_contacto_emergencia": form.cleaned_data['relacion_contacto_emergencia'],
                "numero_telefono_emergencia": form.cleaned_data['numero_telefono_emergencia'],
                "nombre_compania_seguro": form.cleaned_data['nombre_compania_seguro'],
                "numero_poliza_seguro": form.cleaned_data['numero_poliza_seguro'],
                "estado_poliza_seguro": form.cleaned_data['estado_poliza_seguro'],
            }

            # Llama a la API para crear el paciente
            api_url = 'http://127.0.0.1:8000/api/pacientes/create/'
            response = requests.post(api_url, json=data)

            if response.status_code == 201:
                # Si la creación fue exitosa, puedes redirigir o mostrar un mensaje de éxitos
                return redirect('crear_paciente')
            else:
                # Maneja el error de la creación
                messages.error(request, "Hubo un error al crear el paciente a través de la API.")
                print(response)
        else:
            print("Errorcito")
            print(form.errors)
            form = PacienteForm()
    else:
        form = PacienteForm()

    return render(request, 'crear_paciente.html', {'form': form})

@login_required
def buscar_paciente(request):
    if request.method == 'POST':
        numero_identificacion = request.POST.get('numero_identificacion')

        api_url = f'http://127.0.0.1:8000/api/pacientes/{numero_identificacion}/'
        response = requests.get(api_url)

        if response.status_code == 200:
            return redirect('actualizar_paciente', numero_identificacion=numero_identificacion)
        else:
            # Si no se encontró al paciente, muestra un mensaje de error
             messages.error(request, "No se ha encontrado al paciente con el número de identificación proporcionado.")

    return render(request, 'buscar_paciente.html')

@login_required
def actualizar_paciente(request, numero_identificacion):
    # Utiliza el número de identificación para obtener los datos del paciente a través de la API
    api_url = f'http://127.0.0.1:8000/api/pacientes/{numero_identificacion}/'
    response = requests.get(api_url)

    if response.status_code != 200:
        # Si no se encontró al paciente, muestra un mensaje de error
        messages.error(request, "No se ha encontrado al paciente con el número de identificación proporcionado.")
        return redirect('buscar_paciente')

    respuesta = response.json()

    paciente_data = respuesta.get('paciente',{})

    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            # Procesa los datos del formulario y envía una solicitud PUT a la API para actualizar al paciente
            api_update_url = f'http://127.0.0.1:8000/api/pacientes/{numero_identificacion}/update/'

            fecha_nacimiento = form.cleaned_data['fecha_nacimiento'].strftime("%Y-%m-%d")  # Formatea la fecha

            data = {
                "numero_identificacion": form.cleaned_data['numero_identificacion'],
                "nombre_completo": form.cleaned_data['nombre_completo'],
                "fecha_nacimiento": fecha_nacimiento,
                "genero": form.cleaned_data['genero'],
                "direccion": form.cleaned_data['direccion'],
                "numero_telefono": form.cleaned_data['numero_telefono'],
                "correo_electronico": form.cleaned_data['correo_electronico'],
                "nombre_contacto_emergencia": form.cleaned_data['nombre_contacto_emergencia'],
                "relacion_contacto_emergencia": form.cleaned_data['relacion_contacto_emergencia'],
                "numero_telefono_emergencia": form.cleaned_data['numero_telefono_emergencia'],
                "nombre_compania_seguro": form.cleaned_data['nombre_compania_seguro'],
                "numero_poliza_seguro": form.cleaned_data['numero_poliza_seguro'],
                "estado_poliza_seguro": form.cleaned_data['estado_poliza_seguro'],
                "copagos_acumulados": paciente_data['copagos_acumulados'],
            }

            api_response = requests.put(api_update_url, json=data)

            if api_response.status_code == 200:
                # Si la actualización es exitosa, puedes redirigir a una página de confirmación o mostrar un mensaje de éxito
                messages.success(request, "El paciente se ha actualizado con éxito.")
                return redirect('buscar_paciente')
            else:
                # Maneja el error de actualización
                messages.error(request, "Hubo un error al actualizar al paciente a través de la API.")
        else:
            # Si el formulario no es válido, muestra los errores
            messages.error(request, "Existe un valor invalido en el formulario")
    else:
        # Si no se ha enviado el formulario, muestra el formulario de actualización con los datos del paciente
        form = PacienteForm(initial=paciente_data)

    return render(request, 'actualizar_paciente.html', {'form': form, 'numero_identificacion': numero_identificacion})

@login_required
def buscar_paciente_facturacion(request):
    if request.method == 'POST':
        numero_identificacion = request.POST.get('numero_identificacion')

        api_url = f'http://127.0.0.1:8000/api/pacientes/{numero_identificacion}/'
        response = requests.get(api_url)

        if response.status_code == 200:
            return redirect('generar_factura', numero_identificacion=numero_identificacion)
        else:
            # Si no se encontró al paciente, muestra un mensaje de error
             messages.error(request, "No se ha encontrado al paciente con el número de identificación proporcionado.")

    return render(request, 'buscar_paciente_facturacion.html')

def calcular_costo_bruto(historia_clinica):
    costo_bruto = 0

    print(historia_clinica.ordenes.all())

    # Recorrer todas las órdenes en la historia clínica

    for orden in historia_clinica.ordenes.all():
        if orden.tipo_orden == 'medicamento':
            # Si es una orden de medicamento, obtener y sumar el costo de cada medicamento
            orden_medicamento = OrdenMedicamento.objects.get(orden=orden)
            costo_bruto += orden_medicamento.costo
        elif orden.tipo_orden == 'procedimiento':
            # Si es una orden de procedimiento, obtener y sumar el costo de cada procedimiento
            orden_medicamento = OrdenProcedimiento.objects.get(orden=orden)
            costo_bruto += orden_medicamento.costo
        elif orden.tipo_orden == 'hospitalizacion':
           pass
    return costo_bruto

def generar_factura(request, numero_identificacion):
    try:
        paciente = Paciente.objects.get(numero_identificacion=numero_identificacion)
        historia_clinica = HistoriaClinica.objects.filter(paciente=paciente, cerrada = True,pagada=False).first()

        if not historia_clinica:
            return HttpResponse("No hay procedimientos pendientes de facturación para este paciente.")

        # Realizar cálculos para costo_bruto y costo_final
        costo_bruto = calcular_costo_bruto(historia_clinica)
        #costo_final = calcular_costo_final(costo_bruto)

        context = {
            'costo_bruto': costo_bruto,
            'costo_final': paciente.calcular_copago(costo_bruto),
            'numero_identificacion': numero_identificacion
        }

        return render(request, 'facturacion.html', context)
    except Paciente.DoesNotExist:
        return HttpResponse("El paciente no existe.")