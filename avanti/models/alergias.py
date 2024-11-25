from django.db import models

class Alergias(models.Model):
    alergias = models.AutoField(primary_key=True)
    descripcion = models.TextField(blank=True, null=True)
    historial = models.ForeignKey('Historial', on_delete=models.CASCADE, db_column='id_historial')

    class Meta:
        db_table = 'alergias'