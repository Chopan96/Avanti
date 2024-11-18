from django.db import models

class MetodoDePago(models.Model):
    id_metodo = models.CharField(primary_key=True, max_length=20)
    tipo = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'metodo_de_pago'
