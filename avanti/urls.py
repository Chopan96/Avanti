
from django.urls import path
from . import views

app_name = 'administrativo'

urlpatterns = [
    path('', views.home, name='home'),
    path('personal/', views.personal, name='personal'),
    path('disponibilidad/nueva/', views.DisponibilidadCreateView.as_view(), name='registrar_disponibilidad'),



    path('registrar-medico/', views.registrar_medico, name='registrar_medico'),
    path('lista-medicos/', views.lista_medicos, name='lista_medicos'),
    path('paciente/', views.paciente, name='paciente'),
    path('medicos/', views.citas_medicos, name='citas_medicos'),
    path('lista-disponibilidad/', views.lista_disponibilidad, name='lista_disponibilidad'),


    path('api/horarios/', views.HorarioFullCalendarView.as_view(), name='api_horarios'),
    path('generar_horarios/<str:medico_rut>/', views.generar_horarios_view, name='generar_horarios'),
    path('ver-horarios/<str:medico_rut>/', views.ver_horarios, name='ver_horarios'),

]


