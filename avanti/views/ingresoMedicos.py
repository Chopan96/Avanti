from django.shortcuts import render, redirect
from ..forms import UsuarioForm, MedicoForm
from ..models import Medico

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