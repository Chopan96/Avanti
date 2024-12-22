from django.shortcuts import render, redirect,get_object_or_404
from ..models import Horario,Medico,Sala, Horario, Disponibilidad
from django.views import View
from datetime import timedelta,datetime
from django.http import JsonResponse
from datetime import datetime
import pytz
import uuid
from ..forms import GenerarHorarioForm
import json
from django.http import Http404
from rest_framework.views import APIView
from django.utils import timezone
from django.utils.timezone import make_aware
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
# Verificar si el usuario pertenece al grupo 'Personal Administrativo'
def is_personal(user):
    return user.groups.filter(name='Personal Administrativo').exists()

DIAS_MAPA = {
    'Monday': 'L',
    'Tuesday': 'M',
    'Wednesday': 'X',
    'Thursday': 'J',
    'Friday': 'V',
    'Saturday': 'S',
    'Sunday': 'D',
}

@login_required
@user_passes_test(is_personal)

def generar_horario(request, rut_medico):
    try:
        # Obtener el médico mediante su RUT
        medico = Medico.objects.get(usuario__rut=rut_medico)
    except Medico.DoesNotExist:
        return JsonResponse({"error": "Médico no encontrado"}, status=404)

    if request.method == 'POST':
        form = GenerarHorarioForm(request.POST, medico=medico)

        # Obtener el valor de la sucursal seleccionada
        sucursal_id = request.POST.get('sucursal')

        if sucursal_id:
            # Filtrar las salas disponibles según la sucursal seleccionada
            salas_disponibles = Sala.objects.filter(sucursal__sucursal=sucursal_id)
            form.fields['sala'].choices = [(sala.id, sala.sala) for sala in salas_disponibles]
            form.fields['sala'].queryset = salas_disponibles  # Asignar el queryset filtrado de salas

        if form.is_valid():
            sucursal_id = form.cleaned_data['sucursal']
            sala = form.cleaned_data['sala']
            disponibilidades_ids = form.cleaned_data['disponibilidad'].values_list('disponibilidad', flat=True)
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data['fecha_fin']
            hora_inicio = form.cleaned_data['hora_inicio']
            hora_fin = form.cleaned_data['hora_fin']

            # Validar que la fecha de inicio no sea mayor a la fecha de fin
            if fecha_inicio > fecha_fin:
                form.add_error('fecha_inicio', 'La fecha de inicio no puede ser mayor a la fecha de fin.')
                return render(request, 'administrativo/generar_horario.html', {'form': form, 'medico': medico})

            # Traer todas las disponibilidades del médico y filtrar por las seleccionadas
            disponibilidades = Disponibilidad.objects.filter(
                medico=medico, disponibilidad__in=disponibilidades_ids
            )
            
            current_date = fecha_inicio
            while current_date <= fecha_fin:
                day_name = current_date.strftime('%A')  # Día en inglés
                day_initial = DIAS_MAPA.get(day_name)  # Convertir al formato español

                # Filtrar disponibilidades del día correspondiente
                disponibilidades_dia = disponibilidades.filter(dia=day_initial)

                for disponibilidad in disponibilidades_dia:
                    current_time = make_aware(datetime.combine(current_date, hora_inicio))
                    end_time = make_aware(datetime.combine(current_date, hora_fin))

                    while current_time + timedelta(minutes=30) <= end_time:
                        if disponibilidad.horainicio <= current_time.time() <= disponibilidad.horafin:
                            Horario.objects.create(
                                horario=uuid.uuid4(),
                                medico=medico,
                                disponibilidad=disponibilidad,
                                fechainicio=current_time,
                                fechafin=current_time + timedelta(minutes=30),
                                sala=sala,
                                disponible=True
                            )
                        current_time += timedelta(minutes=30)

                current_date += timedelta(days=1)

            messages.success(request, 'Horarios generados exitosamente.')
            return redirect('administrativo:lista_medicos')
        else:
            messages.error(request, 'Corrige los errores en el formulario.')

    else:
        form = GenerarHorarioForm(medico=medico)
    disponibilidades = Disponibilidad.objects.filter(medico=medico)
    return render(request, 'administrativo/generar_horario.html', {'form': form, 'medico': medico})


@login_required
@user_passes_test(is_personal)
def ver_horarios(request, medico_rut):
    medico = get_object_or_404(Medico, usuario__rut=medico_rut)
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
            medico__usuario__rut=medico_rut,
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