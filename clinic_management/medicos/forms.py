from django import forms
from .models import HistoriaClinica,OrdenMedicamento,OrdenProcedimiento, OrdenAyudaDiagnostica
from datetime import date  # Importa la clase date para obtener la fecha actual
from enfermeras.models import Hospitalizacion

class HistoriaClinicaForm(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        fields = ['fecha', 'motivo_consulta', 'sintomatologia', 'diagnostico']

    paciente = forms.CharField(
        label="Cédula del paciente",
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    medico = forms.CharField(
        label="Cédula del médico",
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    fecha = forms.DateField(
        label="Fecha de Creación",
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
        initial=date.today()  # Establece la fecha inicial como la fecha actual
    )

    motivo_consulta = forms.CharField(
        label="Motivo de Consulta",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )

    sintomatologia = forms.CharField(
        label="Sintomatología",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )

    diagnostico = forms.CharField(
        label="Diagnóstico",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )

class OrdenMedicamentoForm(forms.ModelForm):
    class Meta:
        model = OrdenMedicamento
        fields = ['nombre_medicamento', 'dosis', 'duracion_tratamiento', 'costo']

    nombre_medicamento = forms.CharField(
        label='Nombre del Medicamento',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    dosis = forms.CharField(
        label='Dosis',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    duracion_tratamiento = forms.CharField(
        label='Duración del Tratamiento',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    costo = forms.DecimalField(
        label='Costo',
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

class OrdenProcedimientoForm(forms.ModelForm):
    class Meta:
        model = OrdenProcedimiento
        fields = ['nombre_procedimiento', 'numero_veces', 'frecuencia', 'costo', 'requiere_asistencia_especialista']

    nombre_procedimiento = forms.CharField(
        label='Nombre del Procedimiento',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    numero_veces = forms.IntegerField(
        label='Número de Veces',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    frecuencia = forms.CharField(
        label='Frecuencia',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    costo = forms.DecimalField(
        label='Costo',
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    requiere_asistencia_especialista = forms.BooleanField(
        label='Requiere Asistencia de Especialista',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input ml-2'}),
    )

class OrdenAyudaDiagnosticaForm(forms.ModelForm):
    class Meta:
        model = OrdenAyudaDiagnostica
        fields = ['nombre_ayuda_diagnostica', 'cantidad', 'requiere_asistencia_especialista','costo']

    nombre_ayuda_diagnostica = forms.CharField(
        label='Nombre de la Ayuda Diagnóstica',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    cantidad = forms.IntegerField(
        label='Cantidad',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    requiere_asistencia_especialista = forms.BooleanField(
        label='Requiere Asistencia de Especialista',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input ml-2'})
    )

    costo = forms.DecimalField(
        label='Costo',
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

class OrdenAyudaDiagnosticaFinalForm(forms.ModelForm):
    
    class Meta:
        model = OrdenAyudaDiagnostica
        fields = ['resultados']

    resultados = forms.CharField(
        label='Resultados',
        max_length=2000,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )

class OrdenHospitalizacionForm(forms.ModelForm):
    class Meta:
        model = Hospitalizacion
        fields = ['tiempo', 'cantidad_visitas_dia']

    def __init__(self, *args, **kwargs):
        super(OrdenHospitalizacionForm, self).__init__(*args, **kwargs)
        self.fields['tiempo'].widget.attrs.update({'class': 'form-control'})
        self.fields['cantidad_visitas_dia'].widget.attrs.update({'class': 'form-control'})