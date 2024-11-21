from django.shortcuts import render
from ..models import Medico

def citas_medicos(request):
    # Obtiene todos los médicos de la base de datos
    medicos = Medico.objects.all()
    return render(request, 'paciente/Medico.html', {'medicos': medicos})


