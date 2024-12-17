from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import FichaClinica, Consulta

@login_required
def ficha_clinica_paciente(request):
    # Obtener el usuario autenticado
    paciente = request.user.perfil_paciente

    # Obtener la ficha clínica del paciente
    ficha_clinica = get_object_or_404(FichaClinica, paciente=paciente)

    # Obtener las consultas relacionadas con la ficha clínica
    consultas = ficha_clinica.consultas.all()

    context = {
        'ficha_clinica': ficha_clinica,
        'consultas': consultas,
    }
    return render(request, 'paciente/ficha_clinica.html', context)

@login_required
def detalle_paciente_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id, ficha_clinica__paciente=request.user.perfil_paciente)
    
    context = {
        'consulta': consulta,
        'diagnosticos': consulta.diagnosticos.all(),
        'medicamentos': consulta.medicamentos.all(),
        'alergias': consulta.alergias.all(),
        'enfermedades_base': consulta.enfermedades_base.all(),
    }
    return render(request, 'paciente/detalle_consulta.html', context)
