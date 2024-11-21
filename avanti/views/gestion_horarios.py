from django.shortcuts import render
from django.http import JsonResponse,HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from ..models import Horario, Medico
from django.utils.dateparse import parse_datetime




def obtener_horarios(request):
    medico_rut = request.GET.get('medico_rut')  # Obtiene el RUT del médico
    start = request.GET.get('start')  # Fecha de inicio del rango
    end = request.GET.get('end')  # Fecha de fin del rango

    if not medico_rut:
        return HttpResponseBadRequest("RUT no proporcionado.")

    if not start or not end:
        return HttpResponseBadRequest("Rango de fechas no proporcionado.")

    try:
        # Convertir las fechas de string a objetos datetime
        start_date = parse_datetime(start)
        end_date = parse_datetime(end)
        if not start_date or not end_date:
            raise ValueError("Formato de fecha inválido.")

        # Filtrar los horarios del médico en el rango de fechas
        horarios = Horario.objects.filter(
            medico__rut=medico_rut,
            horainicio__gte=start_date,
            horafin__lte=end_date,
        )

        # Formatear los datos en JSON para FullCalendar
        eventos = [
            {
                'title': f"Sala: {horario.sala.nombre}",
                'start': horario.horainicio.isoformat(),
                'end': horario.horafin.isoformat(),
                'extendedProps': {
                    'medico_rut': horario.medico.rut,
                    'sala': horario.sala.nombre,
                    'fecha': horario.fecha.isoformat(),
                }
            }
            for horario in horarios
        ]

        return JsonResponse(eventos, safe=False)

    except ValueError as e:
        return HttpResponseBadRequest(f"Error en las fechas: {e}")

def mostrar_horarios(request):
    """
    Renderiza la página que muestra el calendario filtrado por médico.
    """
    return render(request, 'administrativo/ver_horarios.html') 