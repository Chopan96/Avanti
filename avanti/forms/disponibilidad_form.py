from django import forms
import re
from ..models import Disponibilidad,Medico
from django.core.exceptions import ValidationError
from datetime import time

class DisponibilidadForm(forms.ModelForm):
    class Meta:
        model = Disponibilidad
        fields = ['medico', 'dia', 'horainicio', 'horafin']

        def clean(self):
            cleaned_data = super().clean()
            medico = cleaned_data.get('medico')
            dia = cleaned_data.get('dia')
            horainicio = cleaned_data.get('horainicio')
            horafin = cleaned_data.get('horafin')

            # Validar superposición de horarios
            if medico and dia and horainicio and horafin:
                # Buscar disponibilidades del médico en el mismo día
                disponibilidades = Disponibilidad.objects.filter(medico=medico, dia=dia)

                for disponibilidad in disponibilidades:
                    # Comprobar si el horario se solapa con alguno existente
                    if (horainicio < disponibilidad.horafin and horafin > disponibilidad.horainicio):
                        raise ValidationError(f"Ya existe una disponibilidad del médico {medico.rut} en este horario.")
            
            
            
            # Validar que horafin es posterior a horainicio
            if horainicio and horafin:
                if horainicio >= horafin:
                    raise ValidationError("La hora de fin debe ser posterior a la hora de inicio.")
            
            return cleaned_data

    def clean_horainicio(self):
        horainicio = self.cleaned_data.get('horainicio')

        # Validar que horainicio esté dentro de un rango lógico, por ejemplo entre 08:00 y 18:00
        if horainicio and (horainicio < time(8, 0) or horainicio > time(18, 0)):
            raise ValidationError("La hora de inicio debe estar entre las 08:00 y las 18:00.")

        return horainicio

    def clean_horafin(self):
        horafin = self.cleaned_data.get('horafin')

        # Validar que horafin esté dentro de un rango lógico
        if horafin and (horafin < time(8, 0) or horafin > time(18, 0)):
            raise ValidationError("La hora de fin debe estar entre las 08:00 y las 18:00.")

        return horafin