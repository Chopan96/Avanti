from django import forms
from django.contrib.auth.forms import UserCreationForm
from ..models import Usuario, Medico

class UsuarioForm(UserCreationForm):
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    password2 = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'rut', 'fono', 'password1', 'password2']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
            'rut': 'RUT',
            'fono': 'Teléfono',
        }

    def __init__(self, *args, **kwargs):
        self.is_edit = kwargs.pop('is_edit', False)  # Acepta parámetro para diferenciar creación/edición
        super().__init__(*args, **kwargs)

        # Agregar 'form-control' a todos los campos
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        # Si estamos editando, ocultamos las contraseñas
        if self.is_edit:
            self.fields.pop('password1', None)
            self.fields.pop('password2', None)

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
        if not self.is_edit:  # Solo validamos contraseña en modo creación
            if not password1:
                raise forms.ValidationError("La contraseña es obligatoria.")
            if len(password1) < 8:
                raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
            if password1.isnumeric():
                raise forms.ValidationError("La contraseña no puede ser completamente numérica.")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not self.is_edit and password1 != password2:
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
