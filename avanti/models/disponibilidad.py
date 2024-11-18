from django.db import models

class Disponibilidad(models.Model):
    fecha = models.DateField(blank=True, null=True)
    horainicio = models.DateTimeField(blank=True, null=True)
    horafin = models.DateTimeField(blank=True, null=True)
    medico_rut = models.OneToOneField(
        'Medico', models.CASCADE, db_column='medico_rut', primary_key=True
    )

    class Meta:
        db_table = 'disponibilidad'