from django.db import models


class Pago(models.Model):
    pago = models.CharField(max_length=20)
    monto = models.BigIntegerField(blank=True, null=True)
    fechapago = models.DateField(blank=True, null=True)
    bono = models.ForeignKey(
        'Bono', models.CASCADE, db_column='id_bono'
    )
    metodo = models.ForeignKey(
        'MetodoDePago', models.CASCADE, db_column='id_metodo'
    )
    reporte = models.ForeignKey(
        'Reportes', models.CASCADE, db_column='id_reporte', related_name='pago_id_reporte_set'
    )
    administrativo = models.ForeignKey('Administrativo', models.CASCADE)

    class Meta:
        db_table = 'pago'
        unique_together = (('pago', 'bono', 'reporte', 'administrativo', 'metodo'),)

