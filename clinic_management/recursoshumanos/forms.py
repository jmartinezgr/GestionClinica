# forms.py
from django import forms
from django.contrib.auth.hashers import make_password
from user.models import Usuario
from .models import RegistroAsistencia
from django.utils import timezone
from datetime import date

class UsuarioEditForm(forms.ModelForm):
    nombre = forms.CharField(
        label="Nombres",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    cedula = forms.CharField(
        label="Cedula de Ciudadanía",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    telefono = forms.CharField(
        label="Número de Teléfono",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    nacimiento = forms.DateField(
        label="Fecha de Nacimiento",
        widget=forms.TextInput(attrs={'class': 'form-control', 'type':'date'}),
    )
    nueva_password = forms.CharField(
        label='Nueva Contraseña',
        widget=forms.TextInput(attrs={'class': 'form-control', 'type':'password', 'placeholder': 'Deja en blanco para mantener la contraseña actual'}),
        required=False
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nombre', 'cedula', 'telefono', 'direccion', 'rol', 'nacimiento', 'usuario_activo']

    # ...

    def __init__(self, *args, **kwargs):
        super(UsuarioEditForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['cedula'].widget.attrs.update({'class': 'form-control'})
        self.fields['telefono'].widget.attrs.update({'class': 'form-control'})
        self.fields['direccion'].widget.attrs.update({'class': 'form-control'})
        self.fields['rol'].widget.attrs.update({'class': 'form-control'})
        self.fields['nacimiento'].widget.attrs.update({'class': 'form-control'})
        self.fields['usuario_activo'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['nueva_password'].widget.attrs.update({'class': 'form-control', 'type': 'password', 'placeholder': 'Deja en blanco para mantener la contraseña actual'})

    # ...


    def save(self, commit=True):
        instance = super(UsuarioEditForm, self).save(commit=False)
        nueva_password = self.cleaned_data.get('nueva_password')

        if nueva_password:
            # Si se proporciona una nueva contraseña, encriptarla y establecerla en el modelo
            instance.password = make_password(nueva_password)

        if commit:
            instance.save()
        return instance
    
class RegistroAsistenciaForm(forms.Form):
    
    class Meta:
        model = RegistroAsistencia
        fields = ['fecha', 'usuario'] 

    usuario = forms.CharField(
        label="Usuario", 
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    fecha = forms.DateField(
        label="Fecha de Creación",
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
        initial=date.today()  # Establece la fecha inicial como la fecha actual
    )

