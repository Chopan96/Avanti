from django.http import JsonResponse
from ..models import Paciente

def buscar_paciente(request):
    rut = request.GET.get('rut', '').strip()
    try:
        paciente = Paciente.objects.get(usuario__rut=rut)
        return JsonResponse({'success': True, 'paciente_id': paciente.usuario.id})
    except Paciente.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Paciente no encontrado'})
