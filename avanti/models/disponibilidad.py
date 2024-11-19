from django.db import models

class Disponibilidad(models.Model):
    DIAS_SEMANA = [
        ('L', 'Lunes'),
        ('M', 'Martes'),
        ('X', 'Miércoles'),
        ('J', 'Jueves'),
        ('V', 'Viernes'),
        ('S', 'Sábado'),
        ('D', 'Domingo'),
    ]
    medico_rut = models.OneToOneField(
        'Medico', models.CASCADE, db_column='medico_rut', primary_key=True
    )
    dia = models.CharField(max_length=1, choices=DIAS_SEMANA, default='L')
    horainicio = models.TimeField(blank=True, null=True)
    horafin = models.TimeField(blank=True, null=True)


    class Meta:
        db_table = 'disponibilidad'
        unique_together = ('medico_rut', 'dia', 'horainicio', 'horafin')