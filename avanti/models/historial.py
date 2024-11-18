from django.db import models

class Historial(models.Model):
    id_historial = models.CharField(primary_key=True, max_length=20)
    edad = models.BigIntegerField(blank=True, null=True)
    paciente_rut = models.OneToOneField(
        'Paciente', models.CASCADE, db_column='paciente_rut'
    )

    class Meta:
        db_table = 'historial'