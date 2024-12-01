from django.shortcuts import render, redirect
from ..forms import UsuarioForm, MedicoForm
from ..models import Medico, Usuario
from django.shortcuts import get_object_or_404

def registrar_medico(request):
    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST)
        medico_form = MedicoForm(request.POST)
        if usuario_form.is_valid() and medico_form.is_valid():
            usuario = usuario_form.save(commit=False)
            usuario.tipo = 'medico'  # Asegúrate de que el tipo sea 'medico'
            usuario.save()

            medico = medico_form.save(commit=False)
            medico.rut = usuario  # Relacionar el usuario con el médico
            medico.save()

            return redirect('administrativo:lista_medicos')  # Cambia a la URL deseada
    else:
        usuario_form = UsuarioForm()
        medico_form = MedicoForm()

    return render(request, 'administrativo/ingresar_medicos.html', {
        'usuario_form': usuario_form,
        'medico_form': medico_form,
    })



def lista_medicos(request):
    medicos = Medico.objects.select_related('rut').all()  # Incluye datos del usuario relacionado
    return render(request, 'administrativo/lista_medicos.html', {'medicos': medicos})

def editar_medico(request, rut):
    usuario = get_object_or_404(Usuario, rut=rut)
    medico = get_object_or_404(Medico, rut=usuario)

    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST, instance=usuario)
        medico_form = MedicoForm(request.POST, instance=medico)
        if usuario_form.is_valid() and medico_form.is_valid():
            usuario_form.save()
            medico_form.save()
            return redirect('administrativo:lista_medicos')  # Cambia a la URL deseada
    else:
        usuario_form = UsuarioForm(instance=usuario)
        medico_form = MedicoForm(instance=medico)

    return render(request, 'administrativo/ingresar_medicos.html', {
        'usuario_form': usuario_form,
        'medico_form': medico_form,
    })

def eliminar_medico(request, rut):
    usuario = get_object_or_404(Usuario, rut=rut)
    medico = get_object_or_404(Medico, rut=usuario)

    # Primero elimina al médico, luego al usuario asociado
    medico.delete()
    usuario.delete()

    return redirect('administrativo:lista_medicos') 
