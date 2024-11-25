from django.db import models

class FichaClinica(models.Model):
    id_ficha = models.AutoField(primary_key=True)
    paciente = models.OneToOneField(
        'Paciente', on_delete=models.CASCADE, related_name='ficha_clinica'
    )
    motivo = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'ficha_clinica'