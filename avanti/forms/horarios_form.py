from django import forms
from ..models import Sala, Disponibilidad, Sucursal, Horario
from django.forms import DateInput, TimeInput
from datetime import date, datetime, time
from django.core.exceptions import ValidationError

class GenerarHorarioForm(forms.Form):
    # Campo para seleccionar la sucursal
    sucursal = forms.ChoiceField(
        label='Sucursal',
        choices=[],
        required=True
    )

    # Campo para seleccionar la sala
    sala = forms.ModelChoiceField(
        queryset=Sala.objects.none(),  # Inicialmente vacío, se actualizará dinámicamente
        label='Sala',
        empty_label="Selecciona una sala",
        required=True
    )

    # Campo para seleccionar las disponibilidades del médico (opción múltiple)
    disponibilidad = forms.ModelMultipleChoiceField(
        queryset=Disponibilidad.objects.none(),
        label='Disponibilidad',
        widget=forms.CheckboxSelectMultiple
    )

    # Campo para seleccionar la fecha inicio (no puede ser una fecha anterior al día de hoy)
    fecha_inicio = forms.DateField(
        label='Fecha de Inicio',
        widget=DateInput(attrs={
            'type': 'date',
            'min': date.today().strftime('%Y-%m-%d')  # Establece la fecha mínima como la actual
        }),
        initial=date.today,
        required=True
    )

    # Campo para seleccionar la fecha fin
    fecha_fin = forms.DateField(
        label='Fecha de Fin',
        widget=DateInput(attrs={
            'type': 'date',
            'min': date.today().strftime('%Y-%m-%d')
            }),
        required=True
    )

    # Campo para la hora de inicio
    hora_inicio = forms.TimeField(
        label='Hora de Inicio',
        widget=TimeInput(attrs={'type': 'time'}),
        required=True
    )

    # Campo para la hora de fin
    hora_fin = forms.TimeField(
        label='Hora de Fin',
        widget=TimeInput(attrs={'type': 'time'}),
        required=True
    )

    def __init__(self, *args, medico=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Configurar el onchange para actualizar las salas
        self.fields['sucursal'].widget.attrs['onchange'] = "update_salas()"

        # Filtrar las disponibilidades según el médico proporcionado
        if medico:
            self.fields['disponibilidad'].queryset = Disponibilidad.objects.filter(medico=medico)
        else:
            self.fields['disponibilidad'].queryset = Disponibilidad.objects.none()

        # Cargar las sucursales solo si existen en la base de datos
        try:
            self.fields['sucursal'].choices = [('', 'Selecciona una sucursal')] + [
                (s.sucursal, s.nombre) for s in Sucursal.objects.all()
            ]
        except Exception as e:
            self.fields['sucursal'].choices = [('', 'Selecciona una sucursal')]

    def clean(self):
        cleaned_data = super().clean()

        # Obtener los datos del formulario
        sala = cleaned_data.get('sala')
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')

        # Restricción: la fecha de inicio no puede ser anterior al día actual
        if fecha_inicio and fecha_inicio < date.today():
            raise ValidationError("La fecha de inicio no puede ser un día anterior al día actual.")

        # Restricción: hora de inicio y fin deben estar en el rango de 8:00 a 20:00
        hora_minima = time(8, 0)
        hora_maxima = time(20, 0)

        if hora_inicio and (hora_inicio < hora_minima or hora_inicio > hora_maxima):
            raise ValidationError("La hora de inicio debe estar entre las 8:00 y las 20:00.")

        if hora_fin and (hora_fin < hora_minima or hora_fin > hora_maxima):
            raise ValidationError("La hora de fin debe estar entre las 8:00 y las 20:00.")

        # Validar que fecha y hora de inicio sea menor o igual a fecha y hora de fin
        if fecha_inicio and fecha_fin and hora_inicio and hora_fin:
            fechainicio = datetime.combine(fecha_inicio, hora_inicio)
            fechafin = datetime.combine(fecha_fin, hora_fin)

            if fechainicio > fechafin:
                raise ValidationError("La fecha y hora de inicio deben ser menores o iguales a la fecha y hora de fin.")

            # Validar si ya existe un horario duplicado
            if Horario.objects.filter(
                sala_id=sala,
                fechainicio__lt=fechafin,  # Cualquier horario que comience antes del fin del nuevo horario
                fechafin__gt=fechainicio   # Cualquier horario que termine después del inicio del nuevo horario
            ).exists():
                raise ValidationError("Ya existe un horario que se solapa con este rango de tiempo para la sala seleccionada.")

        return cleaned_data


