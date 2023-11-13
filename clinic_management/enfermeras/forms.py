from django import forms
from .models import Visitas
from medicos.models import HistoriaClinica, OrdenMedicamento

class InformacionAdicionalForm(forms.ModelForm):
    solicitar_otra_visita = forms.BooleanField(required=False, initial=False)
    medicamentos = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Visitas
        fields = ['informacion_adicional', 'temperatura', 'pulso', 'nivel_oxigeno', 'presion_arterial', 'solicitar_otra_visita', 'medicamentos']
        widgets = {
            'informacion_adicional': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'temperatura': forms.TextInput(attrs={'class': 'form-control'}),
            'pulso': forms.TextInput(attrs={'class': 'form-control'}),
            'nivel_oxigeno': forms.TextInput(attrs={'class': 'form-control'}),
            'presion_arterial': forms.TextInput(attrs={'class': 'form-control'}),
            'paciente': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'fecha': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
        }

    def __init__(self, *args, **kwargs):
        super(InformacionAdicionalForm, self).__init__(*args, **kwargs)

        # Rellenar las opciones disponibles para los medicamentos
        historia_clinica = HistoriaClinica.objects.get(paciente=self.instance.paciente)
        ordenes_medicamentos = historia_clinica.ordenes.filter(tipo_orden='medicamento')

        # Construir la lista de opciones como tuplas (value, label)
        medicamentos_choices = [
            (orden.id, str(orden.orden)) for orden in OrdenMedicamento.objects.filter(orden__in=ordenes_medicamentos)
        ]

        self.fields['medicamentos'].queryset = OrdenMedicamento.objects.filter(id__in=[orden[0] for orden in medicamentos_choices])
