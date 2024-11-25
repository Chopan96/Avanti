from django.shortcuts import redirect, render, get_object_or_404
from ..models import FichaClinica, Historial, Alergias, Diagnosticos, EnfermedadesBase, Medicamentos,Paciente
from ..forms import (
    FichaClinicaForm, HistorialForm, AlergiasForm,
    DiagnosticosForm, EnfermedadesBaseForm, MedicamentosForm
)

def buscar_ficha_view(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')
        action = request.POST.get('action')  # Identificar qué botón se presionó

        if action == 'buscar':
            return redirect('administrativo:ficha_clinica', paciente_rut=rut)  # Redirige a la ficha clínica
        elif action == 'crear':
            return redirect('administrativo:crear_ficha', paciente_rut=rut)  # Redirige a crear ficha clínica
    
    return render(request, 'medico/buscar_ficha.html')  # Renderiza el formulario


def crear_ficha_view(request, paciente_rut):
    paciente = get_object_or_404(Paciente, rut=paciente_rut)

    if request.method == 'POST':
        # Crear una nueva ficha clínica
        ficha_form = FichaClinicaForm(request.POST)
        historial_form = HistorialForm(request.POST)

        # Formularios relacionados con historial
        alergias_form = AlergiasForm(request.POST, prefix='alergias')
        diagnosticos_form = DiagnosticosForm(request.POST, prefix='diagnosticos')
        enfermedades_form = EnfermedadesBaseForm(request.POST, prefix='enfermedades')
        medicamentos_form = MedicamentosForm(request.POST, prefix='medicamentos')

        if (ficha_form.is_valid() and historial_form.is_valid() and
            alergias_form.is_valid() and diagnosticos_form.is_valid() and
            enfermedades_form.is_valid() and medicamentos_form.is_valid()):

            # Guardar ficha clínica y asociarla con el paciente
            ficha_clinica = ficha_form.save(commit=False)
            ficha_clinica.paciente = paciente
            ficha_clinica.save()

            # Guardar historial y asociarlo con la ficha clínica
            historial = historial_form.save(commit=False)
            historial.ficha_clinica = ficha_clinica
            historial.save()

            # Guardar datos relacionados con historial
            alergia = alergias_form.save(commit=False)
            alergia.historial = historial
            alergia.save()

            diagnostico = diagnosticos_form.save(commit=False)
            diagnostico.historial = historial
            diagnostico.save()

            enfermedad = enfermedades_form.save(commit=False)
            enfermedad.historial = historial
            enfermedad.save()

            medicamento = medicamentos_form.save(commit=False)
            medicamento.historial = historial
            medicamento.save()

            # Redirigir a la página de la ficha clínica o mostrar mensaje de éxito
            return redirect('ficha_clinica', paciente_rut=paciente_rut)

    else:
        ficha_form = FichaClinicaForm()
        historial_form = HistorialForm()
        alergias_form = AlergiasForm(prefix='alergias')
        diagnosticos_form = DiagnosticosForm(prefix='diagnosticos')
        enfermedades_form = EnfermedadesBaseForm(prefix='enfermedades')
        medicamentos_form = MedicamentosForm(prefix='medicamentos')

    context = {
        'ficha_form': ficha_form,
        'historial_form': historial_form,
        'alergias_form': alergias_form,
        'diagnosticos_form': diagnosticos_form,
        'enfermedades_form': enfermedades_form,
        'medicamentos_form': medicamentos_form,
    }

    return render(request, 'medico/crear_ficha.html', context)

def ficha_clinica_view(request, paciente_rut):
    # Intentar obtener la ficha clínica del paciente
    ficha_clinica = FichaClinica.objects.filter(paciente__rut=paciente_rut).first()

    # Si no existe, redirigir a una página para crear una nueva ficha
    if not ficha_clinica:
        # Redirigir a la vista de creación de la ficha clínica
        return redirect('administrativo:crear_ficha', paciente_rut=paciente_rut)

    # Si la ficha existe, obtener el historial relacionado
    historial = ficha_clinica.historial

    # Formularios principales
    if request.method == 'POST':
        ficha_form = FichaClinicaForm(request.POST, instance=ficha_clinica)
        historial_form = HistorialForm(request.POST, instance=historial)

        # Formularios relacionados con historial
        alergias_form = AlergiasForm(request.POST, prefix='alergias')
        diagnosticos_form = DiagnosticosForm(request.POST, prefix='diagnosticos')
        enfermedades_form = EnfermedadesBaseForm(request.POST, prefix='enfermedades')
        medicamentos_form = MedicamentosForm(request.POST, prefix='medicamentos')

        # Validar y guardar
        if (ficha_form.is_valid() and historial_form.is_valid() and
                alergias_form.is_valid() and diagnosticos_form.is_valid() and
                enfermedades_form.is_valid() and medicamentos_form.is_valid()):

            ficha_form.save()
            historial_form.save()

            # Guardar datos relacionados con historial
            alergia = alergias_form.save(commit=False)
            alergia.historial = historial
            alergia.save()

            diagnostico = diagnosticos_form.save(commit=False)
            diagnostico.historial = historial
            diagnostico.save()

            enfermedad = enfermedades_form.save(commit=False)
            enfermedad.historial = historial
            enfermedad.save()

            medicamento = medicamentos_form.save(commit=False)
            medicamento.historial = historial
            medicamento.save()

            # Redirigir o mostrar un mensaje de éxito
            return render(request, 'ficha_clinica.html', {'success': True})

    else:
        ficha_form = FichaClinicaForm(instance=ficha_clinica)
        historial_form = HistorialForm(instance=historial)
        alergias_form = AlergiasForm(prefix='alergias')
        diagnosticos_form = DiagnosticosForm(prefix='diagnosticos')
        enfermedades_form = EnfermedadesBaseForm(prefix='enfermedades')
        medicamentos_form = MedicamentosForm(prefix='medicamentos')

    context = {
        'ficha_form': ficha_form,
        'historial_form': historial_form,
        'alergias_form': alergias_form,
        'diagnosticos_form': diagnosticos_form,
        'enfermedades_form': enfermedades_form,
        'medicamentos_form': medicamentos_form,
    }

    return render(request, 'ficha_clinica.html', context)