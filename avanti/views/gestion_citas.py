from django.shortcuts import render, get_object_or_404
from ..models import Medico, Horario

def ver_citas(request, medico_rut):
    # Obtener el médico desde la base de datos
    medico = get_object_or_404(Medico, rut__rut=medico_rut)
    
    # Obtener los horarios asociados al médico
    horarios = Horario.objects.filter(medico=medico, disponible=True).order_by('fechainicio')
    
    # Enviar los datos al template
    return render(request, 'paciente/ver_agenda.html', {
        'medico': medico,
        'horarios': horarios,
    })

from django.shortcuts import render

def listar_citas(request):
    horarios = Horario.objects.all()  # Ajusta el filtro según corresponda
    context = {
        'horarios': horarios,
    }
    return render(request, 'listado_citas.html', context)
