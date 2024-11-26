from django.db import models

class Cita(models.Model):
    cita = models.CharField(primary_key=True, max_length=20)
    horario = models.ForeignKey('Horario', on_delete=models.CASCADE, db_column='id_horario', related_name='citas')
    prevision = models.ForeignKey('Prevision', on_delete=models.CASCADE, db_column='id_prevision')
    paciente_rut = models.ForeignKey('Paciente', on_delete=models.CASCADE, db_column='paciente_rut')
    

    class Meta:
        db_table = 'cita'
        unique_together = (('cita', 'paciente_rut', 'prevision'),)

