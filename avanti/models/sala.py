from django.db import models

class Sala(models.Model):
    sala = models.CharField(primary_key=True, max_length=12)
    numero = models.BigIntegerField(blank=True, null=True)
    capacidad = models.BigIntegerField(blank=True, null=True)
    sucursal = models.ForeignKey('Sucursal', on_delete=models.CASCADE, db_column='id_sucursal', related_name='citas')
    class Meta:
        db_table = 'sala'

    def __str__(self):
        return self.sala