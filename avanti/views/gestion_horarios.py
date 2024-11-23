from django.shortcuts import render, redirect,get_object_or_404
from ..models import Horario,Medico,Sala, Horario, Disponibilidad
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import timedelta
from django.http import JsonResponse
from django.utils.timezone import now
from datetime import datetime
import pytz
from ..forms import GenerarHorarioForm



def generar_horarios_view(request, medico_rut):
    medico = get_object_or_404(Medico, rut=medico_rut)

    if request.method == "POST":
        form = GenerarHorarioForm(request.POST)
        if form.is_valid():
            sala = form.cleaned_data["sala"]
            desde = form.cleaned_data["desde"]
            hasta = form.cleaned_data["hasta"]

            # Lógica para generar horarios (usa la función `generar_horarios`)
            horarios = generar_horarios(desde, hasta, medico, sala)

            return JsonResponse({
                "status": "success",
                "message": f"Se generaron {len(horarios)} horarios para el médico {medico.rut}."
            })

        else:
            return JsonResponse({"status": "error", "errors": form.errors}, status=400)

    else:
        form = GenerarHorarioForm()
        return render(request, 'administrativo/generar_horario.html', {'form': form, 'medico': medico})


def generar_horarios(desde, hasta, medico, sala, zona_horaria='America/Santiago'):
    """
    Genera horarios para un médico en un rango de fechas basado en sus disponibilidades.
    """
    horarios_creados = []
    disponibilidades = Disponibilidad.objects.filter(medico=medico)
    tz = pytz.timezone(zona_horaria)
    desde = tz.localize(desde) if desde.tzinfo is None else desde
    hasta = tz.localize(hasta) if hasta.tzinfo is None else hasta

    # Mapeo de los días de la semana al formato usado en el modelo
    DIAS_SEMANA = {
        0: 'L',  # Monday
        1: 'M',  # Tuesday
        2: 'X',  # Wednesday
        3: 'J',  # Thursday
        4: 'V',  # Friday
        5: 'S',  # Saturday
        6: 'D',  # Sunday
    }

    current_date = desde.date()
    end_date = hasta.date()

    while current_date <= end_date:
        dia_semana = DIAS_SEMANA[current_date.weekday()]  # weekday() devuelve un entero (0=Lunes, 6=Domingo)

        disponibilidades_dia = disponibilidades.filter(dia=dia_semana)

        for disponibilidad in disponibilidades_dia:
            start_time = tz.localize(datetime.combine(current_date, disponibilidad.horainicio))
            end_time = tz.localize(datetime.combine(current_date, disponibilidad.horafin))
            start_time = max(start_time, desde)
            end_time = min(end_time, hasta)

            current_start_time = start_time
            while current_start_time + timedelta(minutes=30) <= end_time:
                if not Horario.objects.filter(
                    medico=medico,
                    sala=sala,
                    fechainicio=current_start_time,
                    fechafin=current_start_time + timedelta(minutes=30)
                ).exists():
                    horario = Horario.objects.create(
                        medico=medico,
                        sala=sala,
                        fechainicio=current_start_time,
                        fechafin=current_start_time + timedelta(minutes=30),
                    )
                    horarios_creados.append(horario)

                current_start_time += timedelta(minutes=30)

        current_date += timedelta(days=1)

    return horarios_creados



def ver_horarios(request, medico_rut):
    medico = get_object_or_404(Medico, rut__rut=medico_rut)
    return render(request, 'administrativo/ver_horarios.html', {'medico': medico}) 




class HorarioFullCalendarView(APIView):
    def get(self, request):
        # Obtener el parámetro del médico (ID o RUT)
        medico_rut = request.GET.get('medico', None)

        # Filtrar horarios si se proporciona un médico específico
        horarios = Horario.objects.select_related('medico', 'sala')
        if medico_rut:
            horarios = horarios.filter(medico__rut=medico_rut)

        # Convertir los horarios a un formato compatible con FullCalendar
        events = [
            {
                "title": f"Dr./Dra. {horario.medico.rut.nombre}",
                "start": horario.fechainicio.isoformat(),
                "end": horario.fechafin.isoformat(),
                "description": f"Sala: {horario.sala.numero}"
            }
            for horario in horarios
        ]

        return Response(events)