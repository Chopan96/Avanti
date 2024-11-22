from django import forms
from ..models import Horario, Sala, Medico

class GenerarHorarioForm(forms.Form):
    sala = forms.ModelChoiceField(
        queryset=Sala.objects.all(),
        label="Selecciona la sala",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    desde = forms.DateTimeField(
        label="Fecha de inicio",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
    )
    hasta = forms.DateTimeField(
        label="Fecha de fin",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        desde = cleaned_data.get("desde")
        hasta = cleaned_data.get("hasta")

        if desde and hasta:
            if desde >= hasta:
                raise forms.ValidationError("La fecha de inicio debe ser anterior a la fecha de fin.")

        return cleaned_data