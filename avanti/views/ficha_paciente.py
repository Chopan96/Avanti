from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import FichaClinica, Consulta, Paciente
from django.http import HttpResponseForbidden

import logging
logger = logging.getLogger(__name__)

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test


def is_paciente(user):
    return user.groups.filter(name='Paciente').exists()


@login_required
@user_passes_test(is_paciente)
def ficha_clinica_paciente(request):
    # Obtener el perfil del paciente asociado al usuario autenticado o lanzar 404
    paciente = get_object_or_404(Paciente, usuario=request.user)

    # Obtener la ficha clínica del paciente o lanzar 404
    ficha_clinica = get_object_or_404(FichaClinica, paciente=paciente)

    # Obtener todas las consultas relacionadas con la ficha clínica
    consultas = Consulta.objects.filter(ficha_clinica=ficha_clinica)

    # Contexto para el template
    context = {
        'ficha_clinica': ficha_clinica,
        'consultas': consultas,
    }
    return render(request, 'paciente/ver_ficha.html', context)




@login_required
@user_passes_test(is_paciente)
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
