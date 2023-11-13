from django import forms
from .models import Visitas

class InformacionAdicionalForm(forms.ModelForm):
    solicitar_otra_visita = forms.BooleanField(required=False, initial=False)
    
    class Meta:
        model = Visitas
        fields = ['informacion_adicional', 'temperatura', 'pulso', 'nivel_oxigeno', 'presion_arterial']
        widgets = {
            'informacion_adicional': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'temperatura': forms.TextInput(attrs={'class': 'form-control'}),
            'pulso': forms.TextInput(attrs={'class': 'form-control'}),
            'nivel_oxigeno': forms.TextInput(attrs={'class': 'form-control'}),
            'presion_arterial': forms.TextInput(attrs={'class': 'form-control'}),
            'paciente': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'fecha': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
        }
