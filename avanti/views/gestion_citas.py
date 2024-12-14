from django.shortcuts import render, get_object_or_404, redirect
from ..models import Medico, Horario, Paciente, Prevision, Sucursal, Cita, Usuario, Estado, HistorialEstado
from django.contrib import messages
import re
from django.http import JsonResponse
from datetime import datetime
import logging
from collections import defaultdict
from uuid import UUID
from django.urls import reverse
import uuid
logger = logging.getLogger(__name__)


def normalizar_rut(rut):
    # Eliminar puntos y guiones
    rut_normalizado = re.sub(r'[^0-9]', '', rut)
    return rut_normalizado

def formulario_reserva(request):
    if request.method == 'GET':
        sucursales = Sucursal.objects.all()
        previsiones = Prevision.objects.all()
        return render(request, 'paciente/main.html', {'sucursales': sucursales, 'previsiones': previsiones})

    elif request.method == 'POST':
        rut = request.POST.get('rut')
        sucursal = request.POST.get('sucursal')
        prevision = request.POST.get('prevision')

        # Validar campos obligatorios
        if not (rut and sucursal and prevision):
            logger.error("Todos los campos son obligatorios.")
            return redirect('administrativo:formulario_reserva')

        # Normalizar el RUT
        rut_normalizado = normalizar_rut(rut)

        # Verificar si el usuario existe o crearlo
        usuario, creado_usuario = Usuario.objects.get_or_create(
            rut=rut_normalizado,
            defaults={'first_name': '', 'last_name': '', 'password': '', 'fono': None, 'email': ''}
        )

        if creado_usuario:
            logger.info("Usuario creado automáticamente para proceder con la reserva.")


        paciente, creado_paciente = Paciente.objects.get_or_create(
        usuario=usuario,  # Relación con el modelo Usuario
        defaults={'direccion': ''}
)

        if creado_paciente:
            logger.info("Paciente registrado automáticamente para proceder con la reserva.")

        # Guardar en sesión
        request.session['paciente_rut'] = rut_normalizado
        request.session['sucursal'] = sucursal
        request.session['prevision'] = prevision

        # Redirigir a la página siguiente
        return redirect('administrativo:citas_medicos')

def citas_medicos(request):
    """
    Lista los médicos filtrados por la sucursal seleccionada.
    """
    print(request.session.items())
    sucursal_id = request.session.get('sucursal')
    if not sucursal_id:
        return redirect('administrativo:formulario_reserva')

    # Obtener los médicos asociados a la sucursal
    medicos = Medico.objects.filter(horario__sala__sucursal=sucursal_id).distinct()

    return render(request, 'paciente/Medico.html', {'medicos': medicos})


def ver_citas(request, medico_rut):
    medico = get_object_or_404(Medico, usuario__rut=medico_rut)
    horarios = Horario.objects.filter(medico=medico, disponible=True).order_by('fechainicio')

    # Agrupar los horarios por fecha (solo la fecha, no la hora)
    horarios_por_fecha = {}
    for horario in horarios:
        fecha = horario.fechainicio.date()
        if fecha not in horarios_por_fecha:
            horarios_por_fecha[fecha] = []
        horarios_por_fecha[fecha].append(horario)

    # Pasar timestamp para forzar recarga del archivo JS
    timestamp = datetime.now().timestamp()

    return render(request, 'paciente/ver_agenda.html', {
        'medico': medico,
        'horarios_por_fecha': horarios_por_fecha,
        'timestamp': timestamp,
    })

def reservar_cita(request):
    if request.method == 'POST':
        paciente_rut = request.session.get('paciente_rut')
        prevision_id = request.session.get('prevision')
        horario_id = request.POST.get('horario_id')
        mail = request.POST.get('mail')
        fono = request.POST.get('fono')

        if not (paciente_rut and prevision_id and horario_id and mail and fono):
            return JsonResponse({'success': False, 'error': 'Faltan datos obligatorios para generar la cita.'})

        try:
            # Validar el ID de horario
            horario_uuid = UUID(horario_id)  # Verifica que sea un UUID válido
            horario = get_object_or_404(Horario, horario=horario_uuid)
        except ValueError:
            return JsonResponse({'success': False, 'error': 'El ID de horario no es válido.'})

        if not horario.disponible:
            return JsonResponse({'success': False, 'error': 'El horario seleccionado no está disponible.'})

        try:
            # Actualizar datos de contacto del paciente
            usuario = Usuario.objects.get(rut=paciente_rut)
            usuario.email = mail
            usuario.fono = fono
            usuario.save()

            # Obtener o verificar el paciente
            paciente = get_object_or_404(Paciente, usuario=usuario)

            # Crear un ID único para la cita
            cita_id = f"CITA-{str(horario_id)[:8]}-{paciente_rut}-{prevision_id}-{uuid.uuid4().hex[:8]}"[:100]

            # Crear la cita médica
            cita = Cita.objects.create(
                cita=cita_id,
                horario=horario,
                prevision_id=prevision_id,
                paciente=paciente,
            )

            # Marcar horario como ocupado
            horario.disponible = False
            horario.save()

            # Enviar la redirección como parte de la respuesta JSON
            return JsonResponse({
                'success': True,
                'redirect_url': reverse('administrativo:resumen_cita', args=[cita.cita])
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Ocurrió un error al generar la cita: {str(e)}'})

    return JsonResponse({'success': False, 'error': 'Método no permitido.'})


def resumen_cita(request, cita_id):
    cita = get_object_or_404(Cita, cita=cita_id)
    return render(request, 'paciente/cita.html', {'cita': cita})

def error_cita(request):
    # Obtiene los mensajes de error si existen
    return render(request, 'paciente/error_cita.html')


#Citas ya generadas
def listado_citas(request):
    if request.method == 'POST':
        rut_paciente = request.POST.get('rut')
        try:
            # Buscar el paciente por su RUT
            paciente = get_object_or_404(Paciente, usuario__rut=rut_paciente)

            # Obtener las citas asociadas al paciente
            citas = Cita.objects.filter(paciente=paciente)

            # Verifica que las citas existen
            if not citas.exists():
                messages.warning(request, "No se encontraron citas para este paciente.")
                
            return render(request, 'paciente/listado_cita.html', {'citas': citas})
        except Paciente.DoesNotExist:
            messages.error(request, "Paciente no encontrado. Verifique el RUT.")
            return render(request, 'paciente/listado_cita.html')
    
    return render(request, 'paciente/buscar_rut.html')



def editar_cita(request, medico_rut, cita):
    # Recuperar el médico y la cita asociada
    medico = get_object_or_404(Medico, usuario__rut=medico_rut)
    cita = get_object_or_404(Cita, cita=cita)

    # Obtener paciente y médico relacionados a la cita
    paciente = cita.paciente  # Paciente relacionado a la cita
    medico_cita = cita.horario.medico  # Médico relacionado al horario de la cita

    # Verificar que el médico autenticado es el que pertenece a la cita
    if medico != medico_cita:
        return JsonResponse({'success': False, 'error': 'No tiene permiso para editar esta cita.'}, status=403)

    # Horarios disponibles del médico
    horarios = Horario.objects.filter(medico=medico, disponible=True).order_by('fechainicio')

    # Agrupar los horarios por fecha (solo la fecha, no la hora)
    horarios_por_fecha = {}
    for horario in horarios:
        fecha = horario.fechainicio.date()
        if fecha not in horarios_por_fecha:
            horarios_por_fecha[fecha] = []
        horarios_por_fecha[fecha].append(horario)

    if request.method == 'POST':
        # Obtener datos del formulario
        horario_id = request.POST.get('horario_id')
        mail = request.POST.get('mail')
        fono = request.POST.get('fono')

        if not (horario_id and mail and fono):
            return JsonResponse({'success': False, 'error': 'Faltan datos obligatorios para actualizar la cita.'})

        try:
            # Validar y obtener el horario
            horario_uuid = UUID(horario_id)  # Verifica que sea un UUID válido
            horario = get_object_or_404(Horario, horario=horario_uuid)
        except ValueError:
            return JsonResponse({'success': False, 'error': 'El ID de horario no es válido.'})

        if not horario.disponible:
            return JsonResponse({'success': False, 'error': 'El horario seleccionado no está disponible.'})

        try:
            # Actualizar datos del paciente
            paciente.usuario.email = mail
            paciente.usuario.fono = fono
            paciente.usuario.save()

            # Actualizar la cita con el nuevo horario
            horario_anterior = cita.horario  # Guardar el horario anterior
            cita.horario = horario
            cita.save()

            # Marcar el nuevo horario como ocupado
            horario.disponible = False
            horario.save()

            # Dejar el horario anterior disponible
            horario_anterior.disponible = True
            horario_anterior.save()

            # Redirección exitosa
            return JsonResponse({
                'success': True,
                'redirect_url': reverse('administrativo:resumen_cita', args=[cita.cita])
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Ocurrió un error al actualizar la cita: {str(e)}'})

    # Pasar timestamp para forzar recarga del archivo JS
    timestamp = datetime.now().timestamp()

    # Renderizar el template con los datos necesarios
    return render(request, 'paciente/ver_modificar.html', {
        'cita': cita,
        'horarios_por_fecha': horarios_por_fecha,  # Horarios agrupados por fecha
        'paciente': paciente,  # Datos del paciente
        'medico': medico,  # Información del médico
        'medico_rut': medico.usuario.rut,  # Rut del médico para el template
        'timestamp': timestamp,  # Para recarga del archivo JS
    })




def cancelar_cita(request, cita):

    cita = get_object_or_404(Cita, cita=cita)
    horario = cita.horario
    horario.disponible = True
    horario.save()
    cita.delete()
    messages.success(request, "Cita cancelada exitosamente. El horario está disponible nuevamente.")
    
    return redirect('administrativo:listado_citas')