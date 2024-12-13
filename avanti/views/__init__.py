
from .rutas import personal,home,paciente,medico
from .gestion_disponibilidad import crear_disponibilidad,ver_disponibilidades,editar_disponibilidad,eliminar_disponibilidad
from .gestion_horarios import ver_horarios, HorarioFullCalendarView, generar_horarios_view,EditarHorarioView,EliminarHorarioView
from .ingresoMedicos import registrar_medico,lista_medicos,editar_medico,eliminar_medico
from .gestion_ficha import crear_ficha_view
from .gestion_citas import formulario_reserva,ver_citas, citas_medicos, reservar_cita,resumen_cita, error_cita, cancelar_cita, editar_cita, listado_citas
from .login import CustomLoginView,ingreso

