from django.db import models

class Bono(models.Model):
    bono = models.CharField(primary_key=True, max_length=20)
    monto = models.BigIntegerField(blank=True, null=True)
    feccreacion = models.DateField(blank=True, null=True)
    fecvigencia = models.DateField(blank=True, null=True)
    cita = models.ForeignKey('Cita', on_delete=models.CASCADE, db_column='id_cita')
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE, related_name='bonos')
    prevision = models.ForeignKey('Prevision', on_delete=models.CASCADE, db_column='id_prevision', related_name='bonos')
    reporte = models.ForeignKey('Reportes', on_delete=models.CASCADE, db_column='id_reporte')
    administrativo = models.ForeignKey('Administrativo', on_delete=models.CASCADE)

    class Meta:
        db_table = 'bono'
        unique_together = (('bono', 'reporte', 'administrativo'),)

