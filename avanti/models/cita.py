from django.db import models

class Cita(models.Model):
    cita = models.CharField(primary_key=True, max_length=100)
    horario = models.ForeignKey('Horario', on_delete=models.CASCADE, db_column='id_horario', related_name='citas')
    prevision = models.ForeignKey('Prevision', on_delete=models.CASCADE, db_column='id_prevision')
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE)
    finalizada = models.BooleanField(default=False)

    class Meta:
        db_table = 'cita'
        unique_together = (('cita', 'paciente', 'prevision'),)

