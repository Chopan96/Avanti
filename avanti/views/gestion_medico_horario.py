from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import JsonResponse
from ..models import Medico, Horario, Cita

def is_medico(user):
    return user.groups.filter(name='Medico').exists()

@login_required
@user_passes_test(is_medico)
def ver_horarios_medico(request):
    # Obtener el perfil del médico asociado al usuario logueado
    medico = get_object_or_404(Medico, usuario=request.user)

    # Obtener los horarios asociados al médico
    horarios = Horario.objects.filter(medico=medico).select_related('sala', 'disponibilidad') \
        .prefetch_related('citas')  # Usamos prefetch_related para relaciones inversas

    # Serializar los horarios para enviarlos como JSON al template
    eventos = []
    for horario in horarios:
        color = '#77DD77' if horario.disponible else '#FF6961'  # Verde para disponible, rojo para ocupado
        evento = {
            'id': horario.horario,
            'title': 'Finalizada' if any(cita.finalizada for cita in horario.citas.all()) else ('Disponible' if horario.disponible else 'Ocupado'),
            'start': horario.fechainicio.isoformat(),
            'end': horario.fechafin.isoformat(),
            'backgroundColor': '#CCCCCC' if any(cita.finalizada for cita in horario.citas.all()) else ('#77DD77' if horario.disponible else '#FF6961'),
            'borderColor': '#CCCCCC' if any(cita.finalizada for cita in horario.citas.all()) else ('#77DD77' if horario.disponible else '#FF6961'),
        }
        eventos.append(evento)

    context = {
        'medico': medico,
        'eventos_json': eventos,  # Pasamos los eventos directamente como contexto al template
    }
    return render(request, 'medico/horarios_medico.html', context)

# API para obtener detalles de una cita específica
@login_required
def obtener_detalles_cita(request, horario_id):
    try:
        # Filtrar por el horario y asegurarse de que pertenece al médico logueado
        horario = Horario.objects.get(pk=horario_id, medico__usuario=request.user)
        
        # Obtener la primera cita asociada al horario
        cita = horario.citas.first()
        if cita:
            return JsonResponse({
                'success': True,
                'paciente': cita.paciente.usuario.rut,
                'prevision': cita.prevision.nombre,
                'fecha': horario.fechainicio.strftime('%Y-%m-%d'),
                'hora': horario.fechainicio.strftime('%H:%M'),
                'sala': horario.sala.numero,
            })
        return JsonResponse({'success': False, 'error': 'No hay cita asociada al horario seleccionado.'})
    except Horario.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Horario no encontrado.'})
    
@login_required
@user_passes_test(is_medico)
def finalizar_cita(request, horario_id):
    if request.method == 'POST':
        try:
            # Obtener el horario y verificar que pertenece al médico logueado
            horario = Horario.objects.get(pk=horario_id, medico__usuario=request.user)
            
            # Obtener la primera cita asociada al horario
            cita = horario.citas.first()
            if cita:
                cita.finalizada = True  # Asegúrate de tener este campo en tu modelo
                cita.save()
                return JsonResponse({'success': True, 'message': 'Cita finalizada con éxito.'})
            else:
                return JsonResponse({'success': False, 'error': 'No hay cita asociada al horario.'})
        except Horario.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Horario no encontrado.'})
    return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)
