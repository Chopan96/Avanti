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
        fields = ['medico_rut','dia', 'horainicio', 'horafin']
        widgets = {
            'dia': forms.Select(choices=Disponibilidad.DIAS_SEMANA),
            'horainicio': forms.TimeInput(attrs={'type': 'time'}),
            'horafin': forms.TimeInput(attrs={'type': 'time'}),
        }
