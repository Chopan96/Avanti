from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from ..models import Paciente,Medico,Administrativo
from django.contrib.auth.views import LoginView
from ..forms import CustomLoginForm

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  # Cambia esto según el nombre de tu plantilla
    form_class = CustomLoginForm

    def get_success_url(self):
        user = self.request.user  # Obtener el usuario autenticado
        print(f'Usuario autenticado: {user.rut}')  # Confirmar que se autentica
        print(f'¿Paciente? {Paciente.objects.filter(usuario=user).exists()}')
        print(f'¿Medico? {Medico.objects.filter(usuario=user).exists()}')
        print(f'¿Administrativo? {Administrativo.objects.filter(usuario=user).exists()}')

        # Redirigir según el perfil del usuario
        if hasattr(user, 'perfil_paciente'):
            return reverse_lazy('administrativo:paciente_main')  # Redirige a la URL del main de Paciente
        elif hasattr(user, 'perfil_medico'):
            return reverse_lazy('administrativo:medico_main')  # Redirige a la URL del main de Médico
        elif hasattr(user, 'perfil_administrativo'):
            return reverse_lazy('administrativo:administrativo_main')  # Redirige a la URL del main de Administrativo
        else:
            return reverse_lazy('administrativo:default_main')  # Redirige por defecto si no se encuentra el perfil


# Redirigir al login
def ingreso(request):
    return redirect(reverse_lazy('login'))



