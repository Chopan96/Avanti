from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ..models import Paciente, Usuario
from ..forms import PacienteForm, UsuarioBasicoForm

def listar_pacientes(request):
    """Vista para listar y buscar pacientes."""
    query = request.GET.get('q')
    if query:
        pacientes = Usuario.objects.filter(rut__icontains=query, perfil_paciente__isnull=False)
    else:
        pacientes = Usuario.objects.filter(perfil_paciente__isnull=False)
    return render(request, 'administrativo/lista_pacientes.html', {'pacientes': pacientes, 'query': query})

def gestionar_paciente(request, rut=None):
    """Vista para registrar o editar un paciente."""
    if rut:
        usuario = get_object_or_404(Usuario, rut=rut)
        paciente = getattr(usuario, 'perfil_paciente', None)
    else:
        usuario = Usuario()
        paciente = Paciente()

    if request.method == 'POST':
        usuario_form = UsuarioBasicoForm(request.POST, instance=usuario)
        paciente_form = PacienteForm(request.POST, instance=paciente)
        if usuario_form.is_valid() and paciente_form.is_valid():
            usuario = usuario_form.save()
            paciente = paciente_form.save(commit=False)
            paciente.usuario = usuario
            paciente.save()
            messages.success(request, 'Paciente guardado correctamente.')
            return redirect('administrativo:listar_pacientes')
    else:
        usuario_form = UsuarioBasicoForm(instance=usuario)
        paciente_form = PacienteForm(instance=paciente)

    return render(request, 'administrativo/gestionar_pacientes.html', {
        'usuario_form': usuario_form,
        'paciente_form': paciente_form,
    })
