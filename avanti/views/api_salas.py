from django.http import JsonResponse
from ..models import Sala


def salas_por_sucursal(request, sucursal_id):
    # Filtrar salas por sucursal_id
    salas = Sala.objects.filter(sucursal__sucursal=sucursal_id)  # Filtramos usando 'sucursal' en lugar de 'id_sucursal'
    
    # Crear la respuesta en formato JSON con los datos de las salas
    salas_data = [{'id': sala.id, 'nombre': sala.sala} for sala in salas]
    return JsonResponse({'salas': salas_data})