from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from ..forms import (
    FichaClinicaForm,
    HistorialForm,
    AlergiasForm,
    DiagnosticosForm,
    EnfermedadesBaseForm,
    MedicamentosForm,
)
from ..models import Paciente, FichaClinica, Historial

def crear_ficha_view(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')  # Obtener el RUT del formulario

        # Validar que el RUT no esté vacío
        if not rut:
            messages.error(request, "Debe ingresar un RUT válido.")
            return render(request, 'medico/crear_ficha.html')

        # Verificar si existe el paciente
        paciente = Paciente.objects.filter(usuario__rut=rut).first()
        if not paciente:
            messages.error(request, "Paciente no encontrado.")
            return render(request, 'medico/crear_ficha.html')

        # Verificar si ya existe una ficha clínica
        ficha_clinica = FichaClinica.objects.filter(paciente=paciente).first()

        if ficha_clinica:
            messages.info(request, "Editando ficha clínica existente.")
        else:
            messages.info(request, "Creando nueva ficha clínica.")
            ficha_clinica = FichaClinica(paciente=paciente)

        # Manejar formularios
        ficha_form = FichaClinicaForm(request.POST, instance=ficha_clinica)
        historial_form = HistorialForm(request.POST)
        alergias_form = AlergiasForm(request.POST, prefix='alergias')
        diagnosticos_form = DiagnosticosForm(request.POST, prefix='diagnosticos')
        enfermedades_form = EnfermedadesBaseForm(request.POST, prefix='enfermedades')
        medicamentos_form = MedicamentosForm(request.POST, prefix='medicamentos')

        if (ficha_form.is_valid() and historial_form.is_valid() and
            alergias_form.is_valid() and diagnosticos_form.is_valid() and
            enfermedades_form.is_valid() and medicamentos_form.is_valid()):

            ficha_clinica = ficha_form.save()

            # Obtener o crear historial asociado
            historial, _ = Historial.objects.get_or_create(ficha_clinica=ficha_clinica)

            # Guardar los datos relacionados
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

            messages.success(request, "Ficha clínica guardada exitosamente.")
            return redirect('administrativo:medico_main')

    else:
        # Formularios vacíos para GET
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
