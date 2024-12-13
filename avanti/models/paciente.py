from django.db import models

class Paciente(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE, primary_key=True, related_name='perfil_paciente')
    direccion = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'paciente'
