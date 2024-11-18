from django.db import models


class Pago(models.Model):
    id_pago = models.CharField(max_length=20)
    monto = models.BigIntegerField(blank=True, null=True)
    fechapago = models.DateField(blank=True, null=True)
    id_bono = models.ForeignKey(
        'Bono', models.CASCADE, db_column='id_bono'
    )
    id_metodo = models.ForeignKey(
        'MetodoDePago', models.CASCADE, db_column='id_metodo'
    )
    id_reporte = models.ForeignKey(
        'Reportes', models.CASCADE, db_column='id_reporte', related_name='pago_id_reporte_set'
    )
    administrativo_rut = models.ForeignKey(
        'Administrativo', models.CASCADE, db_column='administrativo_rut', related_name='pago_administrativo_rut_set'
    )

    class Meta:
        db_table = 'pago'
        unique_together = (('id_pago', 'id_bono', 'id_reporte', 'administrativo_rut', 'id_metodo'),)

