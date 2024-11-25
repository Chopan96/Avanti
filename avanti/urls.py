
from django.urls import path
from . import views

app_name = 'administrativo'

urlpatterns = [
    path('', views.home, name='home'),
    path('personal/', views.personal, name='personal'),
    



    path('registrar-medico/', views.registrar_medico, name='registrar_medico'),
    path('lista-medicos/', views.lista_medicos, name='lista_medicos'),
    path('paciente/', views.paciente, name='paciente'),
    path('medicos/', views.citas_medicos, name='citas_medicos'),

    #Disponibilidades
    path('crear-disponibilidad/<str:medico_rut>/', views.crear_disponibilidad, name='crear_disponibilidad'),
    path('ver-disponibilidades/<str:medico_rut>/', views.ver_disponibilidades, name='ver_disponibilidades'),
    path('editar-disponibilidad/<str:disponibilidad_id>/', views.editar_disponibilidad, name='editar_disponibilidad'),
    path('eliminar-disponibilidad/<str:disponibilidad_id>/', views.eliminar_disponibilidad, name='eliminar_disponibilidad'),
    #Horarios
    path('api/horarios/', views.HorarioFullCalendarView.as_view(), name='api_horarios'),
    path('api/horarios/<uuid:horario_id>/editar/', views.EditarHorarioView.as_view(), name='editar_horario'),
    path('api/horarios/<uuid:horario_id>/eliminar/', views.EliminarHorarioView.as_view(), name='eliminar_horario'), 
    path('generar_horarios/<str:medico_rut>/', views.generar_horarios_view, name='generar_horarios'),
    path('ver-horarios/<str:medico_rut>/', views.ver_horarios, name='ver_horarios'),
    #Ficha Clinica
    path('buscar_ficha/', views.buscar_ficha_view, name='buscar_ficha'),
    path('ficha_clinica/<str:paciente_rut>/', views.ficha_clinica_view, name='ficha_clinica'),
    path('crear_ficha/<str:paciente_rut>/', views.crear_ficha_view, name='crear_ficha'),

    #Citas
    path('horarios/<str:medico_rut>/',views.ver_citas, name='ver_citas'),
]


