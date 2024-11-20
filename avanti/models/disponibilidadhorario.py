from django.db import models


class DisponibilidadHorario(models.Model):
    disponibilidad = models.ForeignKey('Disponibilidad', on_delete=models.CASCADE)
    horario = models.ForeignKey('Horario', on_delete=models.CASCADE)

    class Meta:
        db_table = 'disponibilidad_horario'
        unique_together = ('disponibilidad', 'horario')