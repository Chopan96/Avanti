from django import forms
from django.contrib.auth.forms import UserCreationForm
from ..models import Usuario, Medico

class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'rut', 'fono', 'password1', 'password2']
        widgets = {
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        # Personaliza los nombres de los campos en el formulario
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
            'rut': 'RUT',
            'fono': 'Teléfono',
            'password1': 'Contraseña',
            'password2': 'Confirmar Contraseña',
        }
        help_texts = {
            'password1': 'Tu contraseña debe tener al menos 8 caracteres y no puede ser completamente numérica.',
            'password2': 'Introduce la misma contraseña para verificarla.',
        }

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if not rut:
            raise forms.ValidationError("El campo RUT no puede estar vacío.")
        return rut

    def clean(self):
        cleaned_data = super().clean()
        for field_name in ['first_name', 'last_name', 'email', 'rut', 'fono']:
            value = cleaned_data.get(field_name)
            if not value:
                self.add_error(field_name, f"El campo {field_name} no puede estar vacío.")
        return cleaned_data

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1 and len(password1) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if password1 and password1.isnumeric():
            raise forms.ValidationError("La contraseña no puede ser completamente numérica.")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['especialidad']

    def clean_especialidad(self):
        especialidad = self.cleaned_data.get('especialidad')
        if not especialidad:
            raise forms.ValidationError("El campo especialidad no puede estar vacío.")
        return especialidad
