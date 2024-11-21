from django.db import models

class Medicamentos(models.Model):
    medicamentos = models.CharField(primary_key=True, max_length=20)
    nombre = models.TextField(blank=True, null=True)
    historial = models.ForeignKey(
        'Historial', models.CASCADE, db_column='id_historial'
    )

    class Meta:
        db_table = 'medicamentos'
        unique_together = (('medicamentos', 'historial'),)
