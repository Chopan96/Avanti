from django.shortcuts import render, redirect
from ..models import Disponibilidad, Medico
from ..forms import DisponibilidadForm
from django.contrib import messages
from django.views.generic import CreateView

def registrar_disponibilidad(request):
    if request.method == 'POST':
        form = DisponibilidadForm(request.POST)
        if form.is_valid():
            print("Formulario válido:", form.cleaned_data)
            medico_rut = form.cleaned_data['medico_rut']

            # Limpiar el RUT y convertir a mayúsculas (si es necesario)
            medico_rut = medico_rut.replace('-', '').upper()

            try:
                medico = Medico.objects.get(rut=medico_rut)
                disponibilidad = form.save(commit=False)
                disponibilidad.medico = medico
                disponibilidad.save()
                return render(request, 'success.html')
            except Medico.DoesNotExist:
                # Manejar el caso en que no se encuentra al médico
                messages.error(request, "No se encontró un médico con ese RUT.")
                return render(request, 'registrar_disponibilidad.html', {'form': form})
        else:
            print("Errores en el formulario:", form.errors)
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
    

