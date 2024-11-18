from django.db import models

class EnfermedadesBase(models.Model):
    id_enfbase = models.CharField(primary_key=True, max_length=20)
    descripcion = models.TextField(blank=True, null=True)
    id_historial = models.ForeignKey(
        'Historial', models.CASCADE, db_column='id_historial'
    )

    class Meta:
        db_table = 'enfermedades_base'
