from django import forms
from ..models import Paciente, Usuario

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['direccion']
        widgets = {
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'direccion': 'Dirección',
        }

class UsuarioBasicoForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'rut', 'email', 'fono']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'fono': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'rut': 'RUT',
            'email': 'Correo Electrónico',
            'fono': 'Teléfono',
        }
