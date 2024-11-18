from django.db import models

class Horario(models.Model):
    fecha = models.DateField(blank=True, null=True)
    horainicio = models.DateTimeField(blank=True, null=True)
    horafin = models.DateTimeField(blank=True, null=True)
    id_sala = models.ForeignKey(
        'Sala', models.CASCADE, db_column='id_sala'
    )
    medico_rut = models.OneToOneField(
        'Disponibilidad', models.CASCADE, db_column='medico_rut', primary_key=True
    )

    class Meta:
        db_table = 'horario'
        unique_together = (('medico_rut', 'id_sala'),)