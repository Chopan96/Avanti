from django.shortcuts import render, redirect
from ..models import Disponibilidad, Medico
from ..forms import DisponibilidadForm
from django.contrib import messages
from django.views.generic import CreateView

def registrar_disponibilidad(request):
    if request.method == 'POST':
        form = DisponibilidadForm(request.POST)
        if form.is_valid():
            # Procesa el formulario
            # Nota: El RUT no se guarda automáticamente en el modelo porque no pertenece a él
            medico_rut = form.cleaned_data['medico_rut']
            disponibilidad = form.save(commit=False)
            # Aquí podrías asociar el RUT con un médico si tienes un modelo de médicos
            # disponibilidad.medico = Medico.objects.get(rut=medico_rut)  # Ejemplo
            disponibilidad.save()
            return render(request, 'success.html')  # Redirige al éxito
    else:
        form = DisponibilidadForm()

    return render(request, 'registrar_disponibilidad.html', {'form': form})

class DisponibilidadCreateView(CreateView):
    model = Disponibilidad
    form_class = DisponibilidadForm
    template_name = 'administrativo/registrar_disponibilidad.html'

    def form_valid(self, form):
        # Aquí puedes añadir lógica adicional si es necesario.
        return super().form_valid(form)

    def get_success_url(self):
        return redirect('lista_disponibilidades')  # Cambia al nombre de tu URL de éxito.
    

