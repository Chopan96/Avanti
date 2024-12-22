from django.db import models

class Sala(models.Model):
    id = models.AutoField(primary_key=True)  # ID autoincrementable
    sala = models.CharField(max_length=12, blank=True, null=True)  # El campo de sala ahora será opcional
    numero = models.BigIntegerField(blank=True, null=True)
    capacidad = models.BigIntegerField(blank=True, null=True)
    sucursal = models.ForeignKey('Sucursal', on_delete=models.CASCADE, db_column='id_sucursal', related_name='citas')

    class Meta:
        db_table = 'sala'

    def __str__(self):
        return self.sala if self.sala else f"Sala {self.id}"