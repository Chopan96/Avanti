from django import forms
from ..models import Sala

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

        # Validación de campos vacíos
        for field_name in self.fields:
            value = cleaned_data.get(field_name)
            if value is None or (isinstance(value, str) and not value.strip()):
                self.add_error(field_name, f"El campo {field_name} no puede estar vacío.")

        desde = cleaned_data.get("desde")
        hasta = cleaned_data.get("hasta")

        # Validación de rango de fechas
        if desde and hasta:
            if desde >= hasta:
                self.add_error("hasta", "La fecha de inicio debe ser anterior a la fecha de fin.")

        return cleaned_data
