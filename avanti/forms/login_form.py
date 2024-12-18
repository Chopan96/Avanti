from django import forms
from django.contrib.auth.forms import AuthenticationForm
from ..utils import normalizar_rut

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='RUT',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RUT'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )
    def clean_username(self):
        username = self.cleaned_data.get('username')
        rut_normalizado = normalizar_rut(username)
        if not rut_normalizado:
            raise forms.ValidationError("El RUT ingresado no es válido.")
        return rut_normalizado