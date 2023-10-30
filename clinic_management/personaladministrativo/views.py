from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
import requests

from .forms import PacienteForm


@login_required
def home_personal_administrativo(request):
    return render(request, 'personaladministrativo.html', {'user': request.user})

def crear_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            # Recopila los datos del formulario
            data = {
                "numero_identificacion": form.cleaned_data['numero_identificacion'],
                "nombre_completo": form.cleaned_data['nombre_completo'],
                "fecha_nacimiento": form.cleaned_data['fecha_nacimiento'],
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
            response = requests.post('URL_DE_TU_API_PARA_CREAR_PACIENTE', json=data)

            if response.status_code == 201:
                # Si la creación fue exitosa, puedes redirigir o mostrar un mensaje de éxito
                return redirect('pagina_de_exito')
            else:
                # Maneja el error de la creación
                messages.error(request, "Hubo un error al crear el paciente.")
    else:
        form = PacienteForm()

    return render(request, 'crear_paciente.html', {'form': form})
