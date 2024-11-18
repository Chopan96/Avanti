from django.db import models

class Medico(models.Model):
    rut = models.OneToOneField(
        'Usuario', models.CASCADE, db_column='rut', primary_key=True
    )
    especialidad = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'medico'