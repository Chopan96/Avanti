from django.db import models



class Reportes(models.Model):
    id_reporte = models.CharField(primary_key=True, max_length=20)  # The composite primary key (id_reporte, administrativo_rut) found, that is not supported. The first column is selected.
    fechainicio = models.DateField(blank=True, null=True)
    fechafin = models.DateField(blank=True, null=True)
    ingresos = models.BigIntegerField(blank=True, null=True)
    total = models.BigIntegerField(blank=True, null=True)
    administrativo_rut = models.ForeignKey('Administrativo', models.DO_NOTHING, db_column='administrativo_rut')

    class Meta:
        unique_together = (('id_reporte', 'administrativo_rut'),)
