from django.db import models

class Diagnosticos(models.Model):
    diagnostico = models.CharField(primary_key=True, max_length=20)
    descripcion = models.TextField(blank=True, null=True)
    historial = models.ForeignKey(
        'Historial', models.CASCADE, db_column='id_historial'
    )

    class Meta:
        db_table = 'diagnosticos'
        unique_together = (('diagnostico', 'historial'),)