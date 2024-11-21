from django.db import models

class Alergias(models.Model):
    alergias = models.CharField(primary_key=True, max_length=20)
    descripcion = models.TextField(blank=True, null=True)
    id_historial = models.ForeignKey('Historial', on_delete=models.CASCADE, db_column='id_historial')

    class Meta:
        db_table = 'alergias'