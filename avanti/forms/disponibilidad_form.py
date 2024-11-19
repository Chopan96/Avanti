from django import forms
import re
from ..models import Disponibilidad

class DisponibilidadForm(forms.ModelForm):
    # Campo personalizado para el RUT del médico
    medico_rut = forms.CharField(
        max_length=12, 
        required=True, 
        label="RUT del Médico",
        widget=forms.TextInput(attrs={
        'placeholder': 'Ej: 12345678-9',
        'id': 'rutMedico',  # Asegúrate de que el ID coincida con el usado en JS
        'class': 'form-control',})
    )

    field_order = ['medico_rut', 'dia', 'horainicio', 'horafin']

    class Meta:
        model = Disponibilidad
        fields = ['dia', 'horainicio', 'horafin']
        widgets = {
            'dia': forms.Select(choices=Disponibilidad.DIAS_SEMANA),
            'horainicio': forms.TimeInput(attrs={'type': 'time'}),
            'horafin': forms.TimeInput(attrs={'type': 'time'}),
        }

    # Validación personalizada para el RUT
    def clean_medico_rut(self):
        rut = self.cleaned_data.get('medico_rut', '')
        if not self.validar_rut(rut):
            raise forms.ValidationError("El RUT ingresado no es válido.")
        return rut

    def validar_rut(self, rut):
        # Elimina puntos y guiones
        rut = re.sub(r'[^\w]', '', rut)
        if len(rut) < 8:
            return False

        cuerpo = rut[:-1]
        dv = rut[-1].upper()

        # Valida que el cuerpo sea numérico
        if not cuerpo.isdigit():
            return False

        # Calcula el dígito verificador
        suma = 0
        multiplo = 2

        for i in reversed(cuerpo):
            suma += int(i) * multiplo
            multiplo = 9 if multiplo == 7 else multiplo + 1

        resto = suma % 11
        dv_esperado = '0' if resto == 0 else 'K' if resto == 1 else str(11 - resto)

        return dv == dv_esperado
