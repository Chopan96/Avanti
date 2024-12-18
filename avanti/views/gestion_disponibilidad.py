from django.shortcuts import render, redirect,get_object_or_404
from ..models import Disponibilidad, Medico
from ..forms import DisponibilidadForm
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
# Verificar si el usuario pertenece al grupo 'Personal Administrativo'
def is_personal(user):
    return user.groups.filter(name='Personal Administrativo').exists()

@login_required
@user_passes_test(is_personal)
def crear_disponibilidad(request, medico_rut):
    medico = get_object_or_404(Medico, usuario__rut=medico_rut)

    if request.method == 'POST':
        form = DisponibilidadForm(request.POST, medico_rut=medico_rut)
        if form.is_valid():
            disponibilidad = form.save(commit=False)
            disponibilidad.medico = medico  # Asocia el médico correctamente
            disponibilidad.save()
            return redirect('administrativo:ver_disponibilidades', medico_rut=medico.usuario.rut)
    else:
        form = DisponibilidadForm(medico_rut=medico_rut)

    return render(request, 'administrativo/crear_disponibilidad.html', {
        'form': form,
        'medico': medico,
    })

@login_required
@user_passes_test(is_personal)
def ver_disponibilidades(request, medico_rut):
    # Obtiene el objeto Medico usando el rut proporcionado
    medico = get_object_or_404(Medico, usuario__rut=medico_rut)
    
    # Obtiene las disponibilidades asociadas al médico
    disponibilidades = Disponibilidad.objects.filter(medico=medico)

    # Renderiza la plantilla pasando el objeto medico y disponibilidades
    return render(request, 'administrativo/ver_disponibilidades.html', {
        'medico': medico,
        'disponibilidades': disponibilidades
    })

@login_required
@user_passes_test(is_personal)
def editar_disponibilidad(request, disponibilidad_id):
    disponibilidad = get_object_or_404(Disponibilidad, pk=disponibilidad_id)
    medico_rut = disponibilidad.medico.usuario.rut  # Obtener el RUT del médico
    if request.method == 'POST':
        form = DisponibilidadForm(request.POST, instance=disponibilidad, medico_rut=medico_rut)
        if form.is_valid():
            form.save()
            return redirect('administrativo:ver_disponibilidades', medico_rut=medico_rut)
    else:
        form = DisponibilidadForm(instance=disponibilidad, medico_rut=medico_rut)

    return render(request, 'administrativo/editar_disponibilidad.html', {'form': form, 'disponibilidad': disponibilidad})

@login_required
@user_passes_test(is_personal)
def eliminar_disponibilidad(request, disponibilidad_id):
    disponibilidad = get_object_or_404(Disponibilidad, pk=disponibilidad_id)
    medico_rut = disponibilidad.medico.usuario.rut
    disponibilidad.delete()
    return redirect('administrativo:ver_disponibilidades', medico_rut=medico_rut)