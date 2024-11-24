from django.db import models

class Sucursal(models.Model):
    sucursal = models.CharField(primary_key=True, max_length=12)
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()

    class Meta:
        db_table = 'sucursal'