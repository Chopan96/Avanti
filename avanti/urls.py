
from django.urls import path
from . import views

app_name = 'administrativo'

urlpatterns = [
    path('', views.home, name='home'),
    path('personal/', views.personal, name='personal'),
    path('disponibilidad/nueva/', views.DisponibilidadCreateView.as_view(), name='registrar_disponibilidad'),

        # URL del endpoint JSON
    path('api/horarios/', views.obtener_horarios, name='obtener_horarios'),
    # URL de la vista HTML que contiene el calendario
    path('horarios/', views.mostrar_horarios, name='mostrar_horarios'),
    path('registrar-medico/', views.registrar_medico, name='registrar_medico'),
    path('lista-medicos/', views.lista_medicos, name='lista_medicos'),
    path('paciente/', views.paciente, name='paciente'),
    path('medicos/', views.citas_medicos, name='citas_medicos'),
    path('lista-disponibilidad/', views.lista_disponibilidad, name='lista_disponibilidad'),
    path('api/horarios/', views.obtener_horarios, name='obtener_horarios'),
]


