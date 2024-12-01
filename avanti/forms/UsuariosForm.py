from django import forms
from ..models import Usuario, Medico

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['rut', 'nombre', 'apellido', 'password', 'fono', 'mail']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        for field_name in self.fields:
            value = cleaned_data.get(field_name)
            if not value:
                self.add_error(field_name, f"El campo {field_name} no puede estar vacío.")
        return cleaned_data


class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['especialidad']

    def clean_especialidad(self):
        especialidad = self.cleaned_data.get('especialidad')
        if not especialidad:
            raise forms.ValidationError("El campo especialidad no puede estar vacío.")
        return especialidad