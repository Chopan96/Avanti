from django.db import models

class EnfermedadesBase(models.Model):
    enfbase = models.AutoField(primary_key=True)
    descripcion = models.TextField(blank=True, null=True)
    historial = models.ForeignKey(
        'Historial', models.CASCADE, db_column='id_historial'
    )

    class Meta:
        db_table = 'enfermedades_base'
