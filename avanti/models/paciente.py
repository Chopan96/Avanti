from django.db import models

class Paciente(models.Model):
    rut = models.OneToOneField(
        'Usuario', models.CASCADE, db_column='rut', primary_key=True
    )
    direccion = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        db_table = 'paciente'

    
