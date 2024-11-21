from django.db import models
import uuid

class Horario(models.Model):
    horario = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    medico = models.ForeignKey('Medico', on_delete=models.CASCADE)
    disponibilidad = models.ManyToManyField('Disponibilidad', related_name='horarios')
    fecha = models.DateField(blank=True, null=True)
    horainicio = models.DateTimeField(blank=True, null=True)
    horafin = models.DateTimeField(blank=True, null=True)
    sala = models.ForeignKey(
        'Sala', models.CASCADE, db_column='sala'
    )


    class Meta:
        db_table = 'horario'
        unique_together = (('sala','medico', 'fecha', 'horainicio', 'horafin',),)