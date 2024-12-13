from django.db import models

class Historial(models.Model):
    historial =models.AutoField(primary_key=True)
    ficha_clinica = models.OneToOneField(
        'FichaClinica', on_delete=models.CASCADE, related_name='historial'
    )
    edad = models.BigIntegerField(blank=True, null=True)
    

    class Meta:
        db_table = 'historial'

