from django import forms
from ..models import FichaClinica, Consulta, Alergia, Diagnostico, EnfermedadesBase, Medicamento
from datetime import date

class FichaClinicaForm(forms.ModelForm):
    class Meta:
        model = FichaClinica
        fields = ['edad']
        widgets = {
            'edad': forms.NumberInput(attrs={'placeholder': 'Edad del paciente', 'class': 'form-control'}),
        }
        labels = {
            'edad': 'Edad',
        }

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['fecha_consulta', 'motivo', 'observaciones']  # No incluimos 'medico'
        widgets = {
            'fecha_consulta': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Seleccione una fecha...',
                'min': date.today().strftime('%Y-%m-%d')
            }),
            'motivo': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe el motivo de la consulta...', 'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Observaciones del médico...', 'class': 'form-control'}),
        }
        labels = {
            'motivo': 'Motivo de la consulta',
            'observaciones': 'Observaciones',
        }

class AlergiasForm(forms.ModelForm):
    class Meta:
        model = Alergia
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ingrese las alergias del paciente...', 'class': 'form-control'}),
        }
        labels = {
            'descripcion': 'Alergias',
        }

class DiagnosticosForm(forms.ModelForm):
    class Meta:
        model = Diagnostico
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describa los diagnósticos realizados...', 'class': 'form-control'}),
        }
        labels = {
            'descripcion': 'Diagnóstico',
        }

class EnfermedadesBaseForm(forms.ModelForm):
    class Meta:
        model = EnfermedadesBase
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Especifique enfermedades base del paciente...', 'class': 'form-control'}),
        }
        labels = {
            'descripcion': 'Enfermedades Base',
        }

class MedicamentosForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre del medicamento...', 'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Medicamento',
        }

