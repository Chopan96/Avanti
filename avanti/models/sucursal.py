from django.db import models

class Sucursal(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()

    class Meta:
        db_table = 'sucursal'