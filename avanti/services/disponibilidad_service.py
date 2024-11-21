from ..models import Medico, Disponibilidad
from django.core.exceptions import ObjectDoesNotExist

def registrar_disponibilidad_service(medico_rut, form):
    """
    Lógica para registrar una disponibilidad de un médico.
    """
    # Limpiar el RUT (quitar guiones y convertir a mayúsculas)
    medico_rut = medico_rut.replace('-', '').upper()

    try:
        # Obtener la instancia del médico por su RUT
        medico = Medico.objects.get(rut=medico_rut)
        
        # Crear una instancia de Disponibilidad sin guardarla aún
        disponibilidad = form.save(commit=False)
        
        # Asignar la instancia del médico a la disponibilidad
        disponibilidad.medico = medico  # Cambiado de medico_rut a medico
        
        # Guardar la disponibilidad en la base de datos
        disponibilidad.save()
        
        return disponibilidad  # Retorna la disponibilidad registrada

    except Medico.DoesNotExist:
        # Si no se encuentra el médico con ese RUT, retornar None o lanzar un error
        return None