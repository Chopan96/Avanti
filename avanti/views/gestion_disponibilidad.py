from django.shortcuts import render, redirect,get_object_or_404
from ..models import Disponibilidad, Medico
from ..forms import DisponibilidadForm
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse





def crear_disponibilidad(request, medico_rut):
    medico = get_object_or_404(Medico, rut=medico_rut)

    if request.method == 'POST':
        form = DisponibilidadForm(request.POST, medico_rut=medico_rut)
        if form.is_valid():
            form.save()
            return redirect('administrativo:ver_disponibilidades', medico_rut=medico_rut)
    else:
        form = DisponibilidadForm(medico_rut=medico_rut)

    return render(request, 'administrativo/crear_disponibilidad.html', {
        'form': form,
        'medico': medico,
    })

def ver_disponibilidades(request, medico_rut):
    disponibilidades = Disponibilidad.objects.filter(medico__rut=medico_rut)
    medico = Medico.objects.get(rut=medico_rut)
    return render(request, 'administrativo/ver_disponibilidades.html', {'disponibilidades': disponibilidades, 'medico': medico})

def editar_disponibilidad(request, disponibilidad_id):
    disponibilidad = get_object_or_404(Disponibilidad, pk=disponibilidad_id)
    if request.method == 'POST':
        form = DisponibilidadForm(request.POST, instance=disponibilidad)
        if form.is_valid():
            form.save()
            return redirect('administrativo:ver_disponibilidades', medico_rut=disponibilidad.medico.rut)
    else:
        form = DisponibilidadForm(instance=disponibilidad)
    return render(request, 'administrativo/editar_disponibilidad.html', {'form': form, 'disponibilidad': disponibilidad})

def eliminar_disponibilidad(request, disponibilidad_id):
    disponibilidad = get_object_or_404(Disponibilidad, pk=disponibilidad_id)
    medico_rut = disponibilidad.medico.rut
    disponibilidad.delete()
    return redirect('administrativo:ver_disponibilidades', medico_rut=medico_rut)