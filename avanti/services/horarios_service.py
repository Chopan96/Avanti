from datetime import datetime, timedelta
from ..models import Disponibilidad, Horario

def generar_horarios(fecha_inicio, fecha_fin):
    """
    Genera horarios para los médicos a partir de sus disponibilidades.
    
    :param fecha_inicio: Fecha de inicio para generar horarios.
    :param fecha_fin: Fecha de fin para generar horarios.
    """
    disponibilidades = Disponibilidad.objects.all()
    horarios_creados = []

    for disponibilidad in disponibilidades:
        medico = disponibilidad.medico_rut
        dia_semana = disponibilidad.dia
        hora_inicio = disponibilidad.horainicio
        hora_fin = disponibilidad.horafin

        fecha_actual = fecha_inicio
        while fecha_actual <= fecha_fin:
            if fecha_actual.strftime('%A')[0].upper() == dia_semana:
                hora_actual = datetime.combine(fecha_actual, hora_inicio)
                fin_bloque = datetime.combine(fecha_actual, hora_fin)

                while hora_actual < fin_bloque:
                    siguiente_bloque = hora_actual + timedelta(minutes=30)

                    if not Horario.objects.filter(
                        fecha=fecha_actual,
                        horainicio=hora_actual,
                        horafin=siguiente_bloque,
                        medico_rut=disponibilidad
                    ).exists():
                        horario = Horario(
                            fecha=fecha_actual,
                            horainicio=hora_actual,
                            horafin=siguiente_bloque,
                            medico_rut=disponibilidad
                        )
                        horario.save()
                        horarios_creados.append(horario)

                    hora_actual = siguiente_bloque
            fecha_actual += timedelta(days=1)

    return horarios_creados