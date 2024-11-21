import uuid
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
    disponibilidad = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    medico = models.ForeignKey(
        'Medico', on_delete=models.CASCADE, db_column='medico_rut', 
    )
    dia = models.CharField(max_length=1, choices=DIAS_SEMANA, default='L')
    horainicio = models.TimeField(blank=True, null=True)
    horafin = models.TimeField(blank=True, null=True)


    class Meta:
        db_table = 'disponibilidad'
        unique_together = ('medico', 'dia', 'horainicio', 'horafin')