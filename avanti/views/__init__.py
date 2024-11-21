from .rutas import personal,home,paciente
from .gestion_disponibilidad import Disponibilidad,DisponibilidadCreateView,DisponibilidadForm
from .gestion_horarios import generar_horarios_view, mostrar_horarios, obtener_horarios
from .rutas import personal,home
from .gestion_disponibilidad import DisponibilidadCreateView,lista_disponibilidad
from .gestion_horarios import mostrar_horarios, obtener_horarios
from .ingresoMedicos import registrar_medico,lista_medicos
from .gestion_medico import citas_medicos