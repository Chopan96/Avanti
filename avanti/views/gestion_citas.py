from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from ..models import Medico, Horario, Paciente, Prevision, Sucursal, Cita, Usuario
from django.contrib import messages
import re
from datetime import datetime
import logging
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
            defaults={'nombre': '', 'apellido': '', 'password': '', 'fono': None, 'mail': ''}
        )

        if creado_usuario:
            logger.info("Usuario creado automáticamente para proceder con la reserva.")


        # Verificar si el paciente existe o crearlo
        paciente, creado_paciente = Paciente.objects.get_or_create(
            rut=usuario,
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
    medico = get_object_or_404(Medico, rut__rut=medico_rut)
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


def reservar_cita(request, horario_id):
    """
    Procesa la reserva de una cita seleccionada por el paciente.
    """
    paciente_rut = request.session.get('paciente_rut')
    prevision_id = request.session.get('prevision')

    if not (paciente_rut and prevision_id):
        return redirect('administrativo:formulario_reserva')

    horario = get_object_or_404(Horario, horario=horario_id)

    # Validar que el horario esté disponible
    if not horario.disponible:
        return HttpResponseBadRequest("El horario seleccionado ya no está disponible.")

    # Crear la cita
    Cita.objects.create(
        horario=horario,
        prevision_id=prevision_id,
        paciente_rut_id=paciente_rut,
    )

    # Actualizar disponibilidad del horario
    horario.disponible = False
    horario.save()

    # Redirigir a una página de confirmación
    return render(request, 'paciente/confirmacion_cita.html', {'horario': horario})
