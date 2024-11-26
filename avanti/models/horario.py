from django.db import models
import uuid

class Horario(models.Model):
    horario = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    medico = models.ForeignKey('Medico', on_delete=models.CASCADE)
    disponibilidad = models.ManyToManyField('Disponibilidad', related_name='horarios')
    fechainicio = models.DateTimeField(blank=True, null=True)  # Fecha y hora de inicio del evento
    fechafin = models.DateTimeField(blank=True, null=True)    # Fecha y hora de fin del evento
    sala = models.ForeignKey('Sala', models.CASCADE, db_column='id_sala')
    
    disponible = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'horario'
        unique_together = (('sala', 'medico', 'fechainicio', 'fechafin'))