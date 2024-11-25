from django import forms
from ..models import FichaClinica, Historial, Alergias, Diagnosticos, EnfermedadesBase, Medicamentos

class FichaClinicaForm(forms.ModelForm):
    class Meta:
        model = FichaClinica
        fields = ['motivo', 'observaciones']
        widgets = {
            'motivo': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe el motivo de la consulta...'}),
            'observaciones': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Observaciones del médico...'}),
        }
        labels = {
            'motivo': 'Motivo de la consulta',
            'observaciones': 'Observaciones',
        }

class HistorialForm(forms.ModelForm):
    class Meta:
        model = Historial
        fields = ['edad']
        widgets = {
            'edad': forms.NumberInput(attrs={'placeholder': 'Edad del paciente'}),
        }
        labels = {
            'edad': 'Edad',
        }

class AlergiasForm(forms.ModelForm):
    class Meta:
        model = Alergias
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ingrese las alergias del paciente...'}),
        }
        labels = {
            'descripcion': 'Alergias',
        }

class DiagnosticosForm(forms.ModelForm):
    class Meta:
        model = Diagnosticos
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describa los diagnósticos realizados...'}),
        }
        labels = {
            'descripcion': 'Diagnóstico',
        }

class EnfermedadesBaseForm(forms.ModelForm):
    class Meta:
        model = EnfermedadesBase
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Especifique enfermedades base del paciente...'}),
        }
        labels = {
            'descripcion': 'Enfermedades Base',
        }

class MedicamentosForm(forms.ModelForm):
    class Meta:
        model = Medicamentos
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre del medicamento...'}),
        }
        labels = {
            'nombre': 'Medicamento',
        }