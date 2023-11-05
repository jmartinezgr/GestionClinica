from django import forms
from .models import HistoriaClinica,OrdenMedicamento
from datetime import date  # Importa la clase date para obtener la fecha actual

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
