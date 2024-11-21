from django.db import models

class Estado(models.Model):
    estado = models.CharField(primary_key=True, max_length=12)
    descripcion = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = 'estado'