from django.db import models

class Bono(models.Model):
    id_bono = models.CharField(primary_key=True, max_length=20)
    monto = models.BigIntegerField(blank=True, null=True)
    feccreacion = models.DateField(blank=True, null=True)
    fecvigencia = models.DateField(blank=True, null=True)
    id_cita = models.ForeignKey('Cita', on_delete=models.CASCADE, db_column='id_cita')
    paciente_rut = models.ForeignKey('Paciente', on_delete=models.CASCADE, db_column='paciente_rut', related_name='bonos')
    id_prevision = models.ForeignKey('Prevision', on_delete=models.CASCADE, db_column='id_prevision', related_name='bonos')
    id_reporte = models.ForeignKey('Reportes', on_delete=models.CASCADE, db_column='id_reporte')
    administrativo_rut = models.ForeignKey('Administrativo', on_delete=models.CASCADE, db_column='administrativo_rut')

    class Meta:
        db_table = 'bono'
        unique_together = (('id_bono', 'id_reporte', 'administrativo_rut'),)

