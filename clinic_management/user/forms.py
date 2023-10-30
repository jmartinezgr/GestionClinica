from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

class RegistroForm(UserCreationForm):
    nombre = forms.CharField(
        label="Nombres",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    cedula = forms.CharField(
        label="Cedula de Ciudadania",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    telefono = forms.CharField(
        label="Número de Teléfono",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    nacimiento = forms.DateField(
        label="Fecha de Nacimiento",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2', 'nombre', 'cedula', 'telefono', 'direccion', 'rol','nacimiento']

    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['cedula'].widget.attrs.update({'class': 'form-control'})
        self.fields['telefono'].widget.attrs.update({'class': 'form-control'})
        self.fields['direccion'].widget.attrs.update({'class': 'form-control'})
        self.fields['rol'].widget.attrs.update({'class': 'form-control'})
        self.fields['nacimiento'].widget.attrs.update({'class': 'form-control'})
