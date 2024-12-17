from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from ..forms import CustomPasswordChangeForm

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'registration/change_password.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('password_change_done')  # Página de confirmación

    def form_valid(self, form):
        messages.success(self.request, '¡Su contraseña ha sido cambiada con éxito!')
        
        # Redirigir según el perfil del usuario
        user = self.request.user  # Obtener el usuario autenticado
        
        if hasattr(user, 'perfil_paciente'):
            return redirect('administrativo:paciente_main')  # Redirige al main de Paciente
        elif hasattr(user, 'perfil_medico'):
            return redirect('administrativo:medico_main')  # Redirige al main de Médico
        elif hasattr(user, 'perfil_administrativo'):
            return redirect('administrativo:administrativo_main')  # Redirige al main de Administrativo
        else:
            return redirect('administrativo:default_main')  # Redirige por defecto si no se encuentra el perfil

