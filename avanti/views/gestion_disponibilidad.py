from django.shortcuts import render, redirect
from ..models import Disponibilidad, Medico
from ..forms import DisponibilidadForm
from django.contrib import messages
from django.views.generic import CreateView
from ..services import registrar_disponibilidad_service
from django.urls import reverse


def register_disponibilidad(request):
    if request.method == 'POST':
        form = DisponibilidadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('disponibilidad_list')  # Redirect to a list view
    else:
        form = DisponibilidadForm()
    return render(request, 'disponibilidad_form.html', {'form': form})

class DisponibilidadCreateView(CreateView):
    model = Disponibilidad
    form_class = DisponibilidadForm
    template_name = 'administrativo/registrar_disponibilidad.html'

    def form_valid(self, form):
        # ... tu lógica aquí ...
        return super().form_valid(form)

    def get_success_url(self):
        return redirect('lista_disponibilidad/')

def lista_disponibilidad(request):
    disponibilidades = Disponibilidad.objects.all()
    return render(request, 'administrativo/lista_disponibilidad.html', {'disponibilidades': disponibilidades})