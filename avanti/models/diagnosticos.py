from django.db import models

class Diagnosticos(models.Model):
    diagnostico = models.AutoField(primary_key=True)
    descripcion = models.TextField(blank=True, null=True)
    historial = models.ForeignKey(
        'Historial', models.CASCADE, db_column='id_historial'
    )

    class Meta:
        db_table = 'diagnosticos'
