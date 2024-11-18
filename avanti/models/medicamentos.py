from django.db import models

class Medicamentos(models.Model):
    id_medicamentos = models.CharField(max_length=20)
    nombre = models.TextField(blank=True, null=True)
    id_historial = models.ForeignKey(
        'Historial', models.CASCADE, db_column='id_historial'
    )

    class Meta:
        db_table = 'medicamentos'
        unique_together = (('id_medicamentos', 'id_historial'),)
