from django.db import models

class Sala(models.Model):
    sala = models.CharField(primary_key=True, max_length=12)
    numero = models.BigIntegerField(blank=True, null=True)
    capacidad = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'sala'