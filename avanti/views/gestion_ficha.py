from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from ..forms import (
    FichaClinicaForm,
    ConsultaForm,
    AlergiasForm,
    DiagnosticosForm,
    EnfermedadesBaseForm,
    MedicamentosForm,
)
from ..models import Paciente, FichaClinica, Consulta
from ..utils import normalizar_rut
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from ..utils import normalizar_rut  # Asegúrate de tener una función para normalizar el RUT

@login_required
def crear_ficha_view(request):
    # Verificar si el usuario autenticado es un médico
    if not hasattr(request.user, 'perfil_medico'):
        raise PermissionDenied("Solo los médicos pueden acceder a esta vista.")

    medico = request.user.perfil_medico  # Obtener el objeto Médico relacionado con el usuario

    if request.method == 'POST':
        rut = request.POST.get('rut')  # Obtener el RUT del formulario

        # Validar que el RUT no esté vacío
        if not rut:
            messages.error(request, "Debe ingresar un RUT válido.")
            return render(request, 'medico/crear_ficha.html')

        # Normalizar el RUT
        rut_normalizado = normalizar_rut(rut)

        if not rut_normalizado:
            messages.error(request, "El RUT ingresado no es válido.")
            return render(request, 'medico/crear_ficha.html')

        # Verificar si existe el paciente
        paciente = Paciente.objects.filter(usuario__rut=rut_normalizado).first()
        if not paciente:
            messages.error(request, "Paciente no encontrado.")
            return render(request, 'medico/crear_ficha.html')

        # Verificar si ya existe una ficha clínica asociada al paciente
        ficha_clinica = FichaClinica.objects.filter(paciente=paciente).first()

        if ficha_clinica:
            messages.info(request, "Editando ficha clínica existente.")
        else:
            messages.info(request, "Creando nueva ficha clínica.")
            ficha_clinica = FichaClinica(paciente=paciente)

        # Manejar formularios
        ficha_form = FichaClinicaForm(request.POST, instance=ficha_clinica)
        consulta_form = ConsultaForm(request.POST)
        alergias_form = AlergiasForm(request.POST, prefix='alergias')
        diagnosticos_form = DiagnosticosForm(request.POST, prefix='diagnosticos')
        enfermedades_form = EnfermedadesBaseForm(request.POST, prefix='enfermedades')
        medicamentos_form = MedicamentosForm(request.POST, prefix='medicamentos')

        # Validación y guardado
        if (ficha_form.is_valid() and consulta_form.is_valid() and
            alergias_form.is_valid() and diagnosticos_form.is_valid() and
            enfermedades_form.is_valid() and medicamentos_form.is_valid()):
            # Guardar la ficha clínica
            ficha_clinica = ficha_form.save()

            # Crear la consulta
            consulta = consulta_form.save(commit=False)
            consulta.ficha_clinica = ficha_clinica
            consulta.medico = medico  # Asociar la consulta con el médico actual
            consulta.save()

            # Asociar datos relacionados con la consulta
            for form, model_name in zip(
                [alergias_form, diagnosticos_form, enfermedades_form, medicamentos_form],
                ["Alergias", "Diagnósticos", "Enfermedades base", "Medicamentos"]
            ):
                instance = form.save(commit=False)
                instance.consulta = consulta
                instance.save()

            messages.success(request, "Ficha clínica guardada exitosamente.")
            return redirect('administrativo:medico_main')  # Ajusta esta URL según tus necesidades

    else:
        # Formularios vacíos para GET
        ficha_form = FichaClinicaForm()
        consulta_form = ConsultaForm()
        alergias_form = AlergiasForm(prefix='alergias')
        diagnosticos_form = DiagnosticosForm(prefix='diagnosticos')
        enfermedades_form = EnfermedadesBaseForm(prefix='enfermedades')
        medicamentos_form = MedicamentosForm(prefix='medicamentos')

    context = {
        'ficha_form': ficha_form,
        'consulta_form': consulta_form,
        'alergias_form': alergias_form,
        'diagnosticos_form': diagnosticos_form,
        'enfermedades_form': enfermedades_form,
        'medicamentos_form': medicamentos_form,
    }

    return render(request, 'medico/crear_ficha.html', context)



def listado_consultas(request, rut):
    # Normalizar el RUT antes de buscar en la base de datos
    rut_normalizado = normalizar_rut(rut)
    
    # Obtener el paciente usando el RUT normalizado
    paciente = get_object_or_404(Paciente, usuario__rut=rut_normalizado)
    
    # Filtrar las consultas asociadas al paciente
    consultas = Consulta.objects.filter(ficha_clinica__paciente=paciente).select_related('medico')
    
    return render(request, 'medico/listado_consultas.html', {
        'paciente': paciente,
        'consultas': consultas
    })


def detalle_consulta(request, consulta_id):
    # Obtener la consulta específica
    consulta = get_object_or_404(Consulta, id=consulta_id)
    
    return render(request, 'medico/detalle_consulta.html', {
        'consulta': consulta
    })  
