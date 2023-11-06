from django import forms
from .models import Visitas

class InformacionAdicionalForm(forms.ModelForm):
    class Meta:
        model = Visitas
        fields = ['informacion_adicional']
        widgets = {
            'informacion_adicional': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'paciente': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'fecha': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
        }
