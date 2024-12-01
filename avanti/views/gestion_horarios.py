from django.shortcuts import render, redirect,get_object_or_404
from ..models import Horario,Medico,Sala, Horario, Disponibilidad
from django.views import View
from datetime import timedelta,datetime
from django.http import JsonResponse
from datetime import datetime
import pytz
from ..forms import GenerarHorarioForm
import json
from rest_framework.views import APIView
from django.utils import timezone
from django.contrib import messages

def generar_horarios_view(request, medico_rut):
    medico = get_object_or_404(Medico, rut=medico_rut)

    if request.method == "POST":
        form = GenerarHorarioForm(request.POST)
        if form.is_valid():
            sala = form.cleaned_data["sala"]
            desde = form.cleaned_data["desde"]
            hasta = form.cleaned_data["hasta"]

            # Lógica para generar horarios
            horarios = generar_horarios(desde, hasta, medico, sala)

            # Agregar un mensaje de éxito
            messages.success(request, f"Se generaron {len(horarios)} horarios para el médico {medico.rut}.")
            return redirect('administrativo:lista_medicos')
        else:
            # Agregar un mensaje de error con los errores del formulario
            messages.error(request, "Hubo un error al procesar el formulario. Revisa los datos ingresados.")
            return redirect('administrativo:lista_medicos')
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
                        disponibilidad=disponibilidad
                    )
                    horarios_creados.append(horario)

                current_start_time += timedelta(minutes=30)

        current_date += timedelta(days=1)

    return horarios_creados



def ver_horarios(request, medico_rut):
    medico = get_object_or_404(Medico, rut__rut=medico_rut)
    return render(request, 'administrativo/ver_horarios.html', {'medico': medico}) 



class HorarioFullCalendarView(View):
    def get(self, request):
        medico_rut = request.GET.get('medico_rut')
        start = request.GET.get('start')
        end = request.GET.get('end')

        if not medico_rut or not start or not end:
            return JsonResponse({"error": "Faltan parámetros requeridos"}, status=400)

        # Filtrar horarios por médico y rango de fechas
        horarios = Horario.objects.filter(
            medico__rut=medico_rut,
            fechainicio__gte=start,
            fechafin__lte=end
        )

        # Crear la respuesta en el formato esperado por FullCalendar
        data = [
            {
                "id": str(horario.horario),  # Usar el UUID como identificador
                "title": f"Sala {horario.sala.sala}",  # Información adicional opcional
                "start": horario.fechainicio.isoformat(),
                "end": horario.fechafin.isoformat(),
                "editable": True if horario.disponible else False,  # Ejemplo: solo editar si está disponible
            }
            for horario in horarios
        ]

        return JsonResponse(data, safe=False)
#REVISAR ESTE FRAGMENTO DE CODIGO
class EditarHorarioView(APIView):
    def patch(self, request, horario_id):
        try:
            horario = Horario.objects.get(horario=horario_id)
            
            # Extraemos los datos enviados en la solicitud
            data = json.loads(request.body)
            
            # Definir la zona horaria local (ajusta esto según tu zona horaria)
            local_timezone = timezone.get_default_timezone()  # Usa la zona horaria configurada en settings.py
            
            # Actualizamos los campos que vienen en la solicitud
            if 'fechainicio' in data:
                fechainicio_naive = data['fechainicio']
                # Convertir la fecha de ISO 8601 a un objeto datetime (sin zona horaria, naive)
                fechainicio = datetime.fromisoformat(fechainicio_naive)
                
                # Si la fecha ya es aware (tiene zona horaria), la convertimos a naive
                if fechainicio.tzinfo is not None:
                    fechainicio = fechainicio.replace(tzinfo=None)
                
                # Convertir la fecha naive a aware con la zona horaria correcta
                fechainicio_aware = timezone.make_aware(fechainicio, local_timezone)
                horario.fechainicio = fechainicio_aware
                
            if 'fechafin' in data:
                fechafin_naive = data['fechafin']
                # Convertir la fecha de ISO 8601 a un objeto datetime (sin zona horaria, naive)
                fechafin = datetime.fromisoformat(fechafin_naive)
                
                # Si la fecha ya es aware (tiene zona horaria), la convertimos a naive
                if fechafin.tzinfo is not None:
                    fechafin = fechafin.replace(tzinfo=None)
                
                # Convertir la fecha naive a aware con la zona horaria correcta
                fechafin_aware = timezone.make_aware(fechafin, local_timezone)
                horario.fechafin = fechafin_aware
            
            # Guardamos los cambios
            horario.save()
            
            return JsonResponse({'status': 'success', 'message': 'Horario actualizado correctamente'}, status=200)
        
        except Horario.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Horario no encontrado'}, status=404)

class EliminarHorarioView(APIView):
    def delete(self, request, horario_id):
        try:
            horario = Horario.objects.get(horario=horario_id)
            horario.delete()
            return JsonResponse({'status': 'success', 'message': 'Horario eliminado correctamente'}, status=200)
        except Horario.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Horario no encontrado'}, status=404)