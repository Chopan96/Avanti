from django.db import models

class Diagnosticos(models.Model):
    id_diagnostico = models.CharField(max_length=20)
    descripcion = models.TextField(blank=True, null=True)
    id_historial = models.ForeignKey(
        'Historial', models.CASCADE, db_column='id_historial'
    )

    class Meta:
        db_table = 'diagnosticos'
        unique_together = (('id_diagnostico', 'id_historial'),)