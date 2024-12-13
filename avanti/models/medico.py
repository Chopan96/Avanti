from django.db import models

class Medico(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE, primary_key=True,related_name='perfil_medico')
    especialidad = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'medico'