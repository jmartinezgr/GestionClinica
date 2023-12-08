from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
import requests
from .models import Paciente
from medicos.models import *
from .forms import PacienteForm
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from decorators.custom_decorators import role_required

@role_required(['Personal Administrativo','Soporte de Información'])
def home_personal_administrativo(request):
    return render(request, 'personaladministrativo.html', {'user': request.user})

@role_required(['Personal Administrativo','Soporte de Información'])
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
                messages.success(request,'Has creado el paciente de manera exitosa')
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

@role_required(['Personal Administrativo','Soporte de Información'])
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

@role_required(['Personal Administrativo','Soporte de Información'])
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

@role_required(['Personal Administrativo','Soporte de Información'])
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

@role_required(['Personal Administrativo','Soporte de Información'])
def generar_factura(request, numero_identificacion):
    try:
        paciente = Paciente.objects.get(numero_identificacion=numero_identificacion)
        historia_clinica = HistoriaClinica.objects.filter(paciente=paciente, cerrada = True,pagada=False).first()

        if not historia_clinica:
            messages.error(request,"No hay una historia medica por pagar")
            return  redirect('buscar_paciente_facturacion')

        # Realizar cálculos para costo_bruto y costo_final
        costo_bruto = calcular_costo_bruto(historia_clinica)

        context = {
            'costo_bruto': costo_bruto,
            'costo_final': paciente.calcular_copago(costo_bruto),
            'numero_identificacion': numero_identificacion
        }

        if request.method == 'POST':
            paciente.pago()
            historia_clinica.pagada = True
            historia_clinica.save()

            return redirect("buscar_paciente_facturacion")

        return render(request, 'facturacion.html', context)

    except Paciente.DoesNotExist:
        messages.error(request,'Este paciente no existe o no tiene una historia clinica por pagar')
        return  redirect('buscar_paciente_facturacion')

@role_required(['Personal Administrativo','Soporte de Información'])  
def generar_pdf_factura(request, numero_identificacion, costo_bruto):
    costo_bruto = float(costo_bruto)

    try:
        paciente = Paciente.objects.get(numero_identificacion=numero_identificacion)
        historia_clinica = HistoriaClinica.objects.filter(paciente=paciente, cerrada=True, pagada=False).first()

        if not historia_clinica:
            return HttpResponse("No hay procedimientos pendientes de facturación para este paciente.")

        # Crear un objeto PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="factura_procedimientos_{numero_identificacion}.pdf"'
        doc = SimpleDocTemplate(response, pagesize=letter)

        # Crear una lista para los elementos que se añadirán al PDF
        elements = []

        # Crear un estilo para el texto del PDF
        styles = getSampleStyleSheet()
        normal_style = styles['Normal']

        # Agregar información del paciente al PDF
        elements.append(Paragraph("Información del Paciente", normal_style))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Nombre del Paciente: {paciente.nombre_completo}", normal_style))
        elements.append(Paragraph(f"Edad: {paciente.fecha_nacimiento}", normal_style))
        elements.append(Paragraph(f"Cédula: {paciente.numero_identificacion}", normal_style))
        elements.append(Paragraph(f"Medico Tratante: {historia_clinica.medico.nombre}"))
        elements.append(Paragraph(f"Nombre de la Compañia de seguro: {paciente.nombre_compania_seguro}" if paciente.nombre_compania_seguro else "No registra"))
        elements.append(Paragraph(f"Numero de la poliza: {paciente.numero_poliza_seguro}" if paciente.numero_poliza_seguro else "No registra"))
        elements.append(Paragraph(f"Vigencia de la poliza: Activa hasta nuevo aviso") if paciente.estado_poliza_seguro else f"Vigencia de la poliza: Inactiva hasta nuevo aviso")

        # Listar todas las órdenes relacionadas con la historia clínica
        ordenes = historia_clinica.ordenes.all()

        for orden in ordenes:
            elements.append(Spacer(1, 12))
            elements.append(Paragraph(f'Tipo de Orden: {orden.get_tipo_orden_display()}', normal_style))
            elements.append(Paragraph(f'Fecha de Solicitud: {orden.fecha_solicitud}', normal_style))

            if orden.tipo_orden == 'medicamento':
                # Si es una orden de medicamento, obtener y mostrar la información
                elements.append(Paragraph("Detalles de la Orden de Medicamentos", normal_style))
                medicamentos = OrdenMedicamento.objects.filter(orden=orden)
                data = [["Nombre del Medicamento", "Dosis", "Duración del Tratamiento", "Costo"]]
                for medicamento in medicamentos:
                    data.append([medicamento.nombre_medicamento, medicamento.dosis, medicamento.duracion_tratamiento, medicamento.costo])
                table = Table(data)
            elif orden.tipo_orden == 'procedimiento':
                # Si es una orden de procedimiento, obtener y mostrar la información
                elements.append(Paragraph("Detalles de la Orden de Procedimientos", normal_style))
                procedimientos = OrdenProcedimiento.objects.filter(orden=orden)
                data = [["Nombre del Procedimiento", "Número de Veces", "Frecuencia", "Costo"]]
                for procedimiento in procedimientos:
                    data.append([procedimiento.nombre_procedimiento, procedimiento.numero_veces, procedimiento.frecuencia, procedimiento.costo])
                table = Table(data)
            elif orden.tipo_orden == 'ayuda_diagnostica':
                # Si es una orden de ayuda diagnóstica, obtener y mostrar la información
                elements.append(Paragraph("Detalles de la Orden de Ayuda Diagnóstica", normal_style))
                ayudas_diagnosticas = OrdenAyudaDiagnostica.objects.filter(orden=orden)
                data = [["Nombre de la Ayuda", "Cantidad", "Resultados", "Costo"]]
                for ayuda_diagnostica in ayudas_diagnosticas:
                    data.append([ayuda_diagnostica.nombre_ayuda_diagnostica, ayuda_diagnostica.cantidad, ayuda_diagnostica.resultados, ayuda_diagnostica.costo])
                table = Table(data)

            # Establecer un ancho fijo para todas las celdas de la tabla
            # Establecer un ancho fijo para todas las celdas de la tabla
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('WIDTH', (0, 0), (-1, -1), 60),  # Ancho fijo para todas las celdas
            ]))

            elements.append(table)

        # Agregar el costo final al PDF
        elements.append(Spacer(1, 20))
        elements.append(Paragraph(f'Costo Bruto: {costo_bruto}', normal_style))
        elements.append(Paragraph(f'Costo Final: {paciente.calcular_copago(costo_bruto)}', normal_style))

        doc.build(elements)

        return response
    except Paciente.DoesNotExist:
        messages.error(request,"El paciente no existe")        
        return  redirect('buscar_paciente_facturacion')
