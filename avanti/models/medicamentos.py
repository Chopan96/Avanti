from django.db import models

class Medicamentos(models.Model):
    medicamentos = models.AutoField(primary_key=True)
    nombre = models.TextField(blank=True, null=True)
    historial = models.ForeignKey(
        'Historial', models.CASCADE, db_column='id_historial'
    )

    class Meta:
        db_table = 'medicamentos'

