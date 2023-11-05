from django import forms
from .models import HistoriaClinica
from datetime import date  # Importa la clase date para obtener la fecha actual

class HistoriaClinicaForm(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        fields = ['paciente', 'fecha', 'motivo_consulta', 'sintomatologia', 'diagnostico', 'medico']

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
