from django.db import models


class Prevision(models.Model):
    prevision = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    tipo = models.CharField(max_length=50, blank=True, null=True)
    cobertura = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'prevision'