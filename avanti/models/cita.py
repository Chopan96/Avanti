from django.db import models

class Cita(models.Model):
    id_cita = models.CharField(primary_key=True, max_length=20)
    hora = models.DateField(blank=True, null=True)
    id_prevision = models.ForeignKey('Prevision', on_delete=models.CASCADE, db_column='id_prevision')
    id_sala = models.ForeignKey('Sala', on_delete=models.CASCADE, db_column='id_sala')
    medico_rut = models.ForeignKey('Medico', on_delete=models.CASCADE, db_column='medico_rut', related_name='citas')
    paciente_rut = models.ForeignKey('Paciente', on_delete=models.CASCADE, db_column='paciente_rut')

    class Meta:
        db_table = 'cita'
        unique_together = (('id_cita', 'paciente_rut', 'id_prevision'),)

