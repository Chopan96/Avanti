from django import forms
from ..models import Disponibilidad
from django.core.exceptions import ValidationError
from datetime import time

class DisponibilidadForm(forms.ModelForm):
    class Meta:
        model = Disponibilidad
        fields = ['medico', 'dia', 'horainicio', 'horafin']

    def __init__(self, *args, **kwargs):
        medico_rut = kwargs.pop('medico_rut', None)  # Recibe el rut del médico como argumento
        super().__init__(*args, **kwargs)
        if medico_rut:
            # Inicializar el campo 'medico' con el rut recibido
            self.fields['medico'].initial = medico_rut
            self.fields['medico'].widget = forms.TextInput(attrs={'readonly': 'readonly'})  # Solo lectura

    def clean(self):
        cleaned_data = super().clean()
        medico = cleaned_data.get('medico')
        dia = cleaned_data.get('dia')
        horainicio = cleaned_data.get('horainicio')
        horafin = cleaned_data.get('horafin')

        # Validar superposición de horarios excluyendo la instancia actual
        if medico and dia and horainicio and horafin:
            disponibilidades = Disponibilidad.objects.filter(medico=medico, dia=dia).exclude(disponibilidad=self.instance.disponibilidad)
            for disponibilidad in disponibilidades:
                if horainicio < disponibilidad.horafin and horafin > disponibilidad.horainicio:
                    raise ValidationError(f"Ya existe una disponibilidad del médico {medico.rut} en este horario.")

        # Validar que horafin es posterior a horainicio
        if horainicio and horafin and horainicio >= horafin:
            raise ValidationError("La hora de fin debe ser posterior a la hora de inicio.")

        return cleaned_data

    def clean_horainicio(self):
        horainicio = self.cleaned_data.get('horainicio')
        if horainicio and (horainicio < time(8, 0) or horainicio > time(18, 0)):
            raise ValidationError("La hora de inicio debe estar entre las 08:00 y las 18:00.")
        return horainicio

    def clean_horafin(self):
        horafin = self.cleaned_data.get('horafin')
        if horafin and (horafin < time(8, 0) or horafin > time(18, 0)):
            raise ValidationError("La hora de fin debe estar entre las 08:00 y las 18:00.")
        return horafin