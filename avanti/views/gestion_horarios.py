from django.shortcuts import render
from ..services.disponibilidad_service import generar_horarios
from datetime import date
from django.http import JsonResponse
from ..models import Horario

def generar_horarios_view(request):
    if request.method == 'POST':
        fecha_inicio = date.fromisoformat(request.POST['fecha_inicio'])
        fecha_fin = date.fromisoformat(request.POST['fecha_fin'])
        horarios = generar_horarios(fecha_inicio, fecha_fin)
        return JsonResponse({'status': 'success', 'horarios_creados': len(horarios)})



def obtener_horarios(request):
    medico_rut = request.GET.get('medico_rut', None)  # Captura el RUT desde la URL
    if medico_rut:
        horarios = Horario.objects.filter(medico_rut=medico_rut)  # Filtra por RUT del médico
    else:
        horarios = Horario.objects.all()  # Si no se pasa RUT, devuelve todos (opcional)

    # Convierte los horarios a un formato JSON para el FullCalendar
    events = [
        {
            "title": f"Horario en sala {horario.id_sala.id}",
            "start": horario.horainicio.isoformat(),
            "end": horario.horafin.isoformat(),
            "extendedProps": {
                "fecha": horario.fecha.isoformat(),
                "sala": horario.id_sala.nombre
            },
        }
        for horario in horarios
    ]
    return JsonResponse(events, safe=False)


def mostrar_horarios(request):
    """
    Renderiza la página que muestra el calendario filtrado por médico.
    """
    return render(request, 'administrativo/ver_horarios.html') 