from django import forms
from ..models import Usuario, Medico

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['rut', 'nombre', 'apellido', 'password', 'fono', 'mail']
        widgets = {
            'password': forms.PasswordInput(),
        }

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['especialidad']