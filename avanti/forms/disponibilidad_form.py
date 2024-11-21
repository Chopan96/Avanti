from django import forms
import re
from ..models import Disponibilidad,Medico
from django.core.exceptions import ValidationError

class DisponibilidadForm(forms.ModelForm):
    class Meta:
        model = Disponibilidad
        fields = '__all__'