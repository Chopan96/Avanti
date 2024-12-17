from django import forms
from ..models import Disponibilidad, Medico
from django.core.exceptions import ValidationError
from datetime import time

class DisponibilidadForm(forms.ModelForm):
    medico_rut = forms.CharField(max_length=12, label="RUT del Médico", widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    horainicio = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        label="Hora de inicio"
    )
    horafin = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        label="Hora de fin"
    )
    dia = forms.ChoiceField(
        choices=Disponibilidad.DIAS_SEMANA,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Día de la semana"
    )
    class Meta:
        model = Disponibilidad
        fields = ['medico_rut', 'dia', 'horainicio', 'horafin']

    def __init__(self, *args, **kwargs):
        medico_rut = kwargs.pop('medico_rut', None)
        super().__init__(*args, **kwargs)
        if medico_rut:
            self.fields['medico_rut'].initial = medico_rut

    def clean_medico_rut(self):
        rut = self.cleaned_data.get('medico_rut')
        try:
            medico = Medico.objects.get(usuario__rut=rut)
            return medico
        except Medico.DoesNotExist:
            raise ValidationError(f"No se encontró un médico con el RUT: {rut}")

    def save(self, commit=True):
        medico = self.cleaned_data.get('medico_rut')  # Esto ya es una instancia de Medico
        self.instance.medico = medico  # Asigna el médico al campo de la instancia
        return super().save(commit=commit)
