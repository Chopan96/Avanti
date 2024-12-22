from django import forms
from django.core.exceptions import ValidationError
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
        error_messages = {
            'direccion': {
                'required': 'La dirección es obligatoria.',
            }
        }

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion')
        if not direccion.strip():  # Verificar que no sea solo espacios
            raise ValidationError('Este campo no puede estar vacío o contener solo espacios.')
        return direccion


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
        error_messages = {
            'first_name': {'required': 'El nombre es obligatorio.'},
            'last_name': {'required': 'El apellido es obligatorio.'},
            'rut': {'required': 'El RUT es obligatorio.', 'invalid': 'El RUT ingresado no es válido.'},
            'email': {'required': 'El correo electrónico es obligatorio.', 'invalid': 'Ingresa un correo válido.'},
            'fono': {'required': 'El teléfono es obligatorio.', 'invalid': 'Ingresa un número de teléfono válido.'},
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.strip():
            raise ValidationError('Este campo no puede estar vacío o contener solo espacios.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.strip():
            raise ValidationError('Este campo no puede estar vacío o contener solo espacios.')
        return last_name

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if not rut.strip():
            raise ValidationError('Este campo no puede estar vacío o contener solo espacios.')
        # Aquí podrías agregar validaciones adicionales para el formato del RUT
        return rut

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.strip():
            raise ValidationError('Este campo no puede estar vacío o contener solo espacios.')
        return email

    def clean_fono(self):
        fono = self.cleaned_data.get('fono')
        if not fono:
            raise ValidationError('Este campo no puede estar vacío.')
        if len(str(fono)) < 8:
            raise ValidationError('El número de teléfono debe tener al menos 8 dígitos.')
        return fono

