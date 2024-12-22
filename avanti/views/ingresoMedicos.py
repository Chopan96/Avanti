from django.shortcuts import render, redirect
from ..forms import UsuarioForm, MedicoForm, UsuarioEditForm
from ..models import Medico, Usuario
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import Group
from django.contrib import messages

# Verificar si el usuario pertenece al grupo 'Personal Administrativo'
def is_personal(user):
    return user.groups.filter(name='Personal Administrativo').exists()

@login_required
@user_passes_test(is_personal)
def registrar_medico(request):
    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST)
        medico_form = MedicoForm(request.POST)
        
        try:
            if usuario_form.is_valid() and medico_form.is_valid():
                usuario = usuario_form.save(commit=False)
                usuario.set_password(usuario_form.cleaned_data['password1'])  # Guarda contraseña
                usuario.save()

                grupo_medico = Group.objects.get(name='Medico')  # Asegúrate de que este grupo exista
                usuario.groups.add(grupo_medico)

                medico = medico_form.save(commit=False)
                medico.usuario = usuario  # Relaciona el médico con el usuario


                medico.save()

                messages.success(request, "Médico registrado exitosamente.")
                return redirect('administrativo:lista_medicos')  # Cambia a la URL deseada
        except ValueError as e:
            # Captura el error de RUT no válido y lo añade como mensaje de error
            messages.error(request, str(e))

    else:
        usuario_form = UsuarioForm()
        medico_form = MedicoForm()

    return render(request, 'administrativo/ingresar_medicos.html', {
        'usuario_form': usuario_form,
        'medico_form': medico_form,
    })



@login_required
@user_passes_test(is_personal)
def lista_medicos(request):
    medicos = Medico.objects.select_related('usuario').all()  # Incluye datos del usuario relacionado
    return render(request, 'administrativo/lista_medicos.html', {'medicos': medicos})

@login_required
@user_passes_test(is_personal)
def editar_medico(request, rut):
    usuario = get_object_or_404(Usuario, rut=rut)
    medico = get_object_or_404(Medico, usuario=usuario)

    if request.method == 'POST':
        usuario_form = UsuarioEditForm(request.POST, instance=usuario)
        medico_form = MedicoForm(request.POST, instance=medico)
        if usuario_form.is_valid() and medico_form.is_valid():
            usuario_form.save()
            medico_form.save()
            return redirect('administrativo:lista_medicos')  # Cambia a la URL deseada
    else:
        usuario_form = UsuarioEditForm(instance=usuario)
        medico_form = MedicoForm(instance=medico)

    return render(request, 'administrativo/ingresar_medicos.html', {
        'usuario_form': usuario_form,
        'medico_form': medico_form,
        'is_edit': True
    })

@login_required
@user_passes_test(is_personal)
def eliminar_medico(request, rut):
    usuario = get_object_or_404(Usuario, rut=rut)
    medico = get_object_or_404(Medico, usuario=usuario)

    # Primero elimina al médico, luego al usuario asociado
    medico.delete()
    usuario.delete()

    return redirect('administrativo:lista_medicos') 
