from django.contrib.auth.views import LogoutView
from django.urls import path,reverse_lazy
from . import views

app_name = 'administrativo'

urlpatterns = [
    #Login
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('default_main')), name='logout'),

    path('paciente/', views.paciente, name='paciente_main'),
    path('medico/', views.medico, name='medico_main'),
    path('administrativo/', views.personal, name='administrativo_main'),
    path('', views.home, name='default_main'),

    #Medicos desde vista administrativo
    path('registrar-medico/', views.registrar_medico, name='registrar_medico'),
    path('lista-medicos/', views.lista_medicos, name='lista_medicos'),
    path('editar_medico/<str:rut>/', views.editar_medico, name='editar_medico'),
    path('eliminar_medico/<str:rut>/', views.eliminar_medico, name='eliminar_medico'),

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
    
    path('crear_ficha/', views.crear_ficha_view, name='crear_ficha'),

    #Citas
    
    path('formulario-reserva/', views.formulario_reserva, name='formulario_reserva'),
    path('medicos/', views.citas_medicos, name='citas_medicos'),
    path('horarios/<str:medico_rut>/', views.ver_citas, name='ver_citas'),
    path('reservar_cita/', views.reservar_cita, name='reservar_cita'),
    path('resumen-cita/<str:cita_id>/', views.resumen_cita, name='resumen_cita'),
    path('error/', views.error_cita, name='error_cita'),

    #Citas ya generadas
    path('citas/listado/', views.listado_citas, name='listado_citas'),
    path('buscar/rut/', views.listado_citas, name='buscar_rut'),  # Vista para ingresar el RUT
    path('editar_cita/<str:medico_rut>/<str:cita>/', views.editar_cita, name='editar_cita'),
    path('cita/cancelar/<str:cita>/', views.cancelar_cita, name='cancelar_cita'),
]



