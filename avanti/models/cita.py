from django.db import models

class Cita(models.Model):
    cita = models.CharField(primary_key=True, max_length=20)
    hora = models.DateField(blank=True, null=True)
    prevision = models.ForeignKey('Prevision', on_delete=models.CASCADE, db_column='id_prevision')
    sala = models.ForeignKey('Sala', on_delete=models.CASCADE, db_column='id_sala')
    medico_rut = models.ForeignKey('Medico', on_delete=models.CASCADE, db_column='medico_rut', related_name='citas')
    paciente_rut = models.ForeignKey('Paciente', on_delete=models.CASCADE, db_column='paciente_rut')
    sucursal = models.ForeignKey('Sucursal', on_delete=models.CASCADE, db_column='id_sucursal', related_name='citas')

    class Meta:
        db_table = 'cita'
        unique_together = (('cita', 'paciente_rut', 'prevision'),)

