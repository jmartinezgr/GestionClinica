from django import forms

class PacienteForm(forms.Form):
    numero_identificacion = forms.CharField(
        label="Número de Identificación", max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    nombre_completo = forms.CharField(
        label="Nombre Completo", max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    fecha_nacimiento = forms.DateField(
        label="Fecha de Nacimiento",
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    genero = forms.ChoiceField(
        label="Género",
        choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('Otro', 'Otro')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    direccion = forms.CharField(
        label="Dirección", max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    numero_telefono = forms.CharField(
        label="Número de Teléfono", max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    correo_electronico = forms.EmailField(
        label="Correo Electrónico", required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    nombre_contacto_emergencia = forms.CharField(
        label="Nombre de Contacto de Emergencia", max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    relacion_contacto_emergencia = forms.CharField(
        label="Relación con el Paciente", max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    numero_telefono_emergencia = forms.CharField(
        label="Número de Teléfono de Emergencia", max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    nombre_compania_seguro = forms.CharField(
        label="Nombre de la Compañía ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    numero_poliza_seguro = forms.CharField(
        label="Número de Póliza de Seguro",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    estado_poliza_seguro = forms.BooleanField(
        label="Estado de la Póliza", required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )