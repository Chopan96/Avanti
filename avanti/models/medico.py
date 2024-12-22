from django.db import models

class Medico(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE, primary_key=True, related_name='perfil_medico')
    especialidad = models.ForeignKey('Especialidad', on_delete=models.PROTECT, related_name='medicos')

    class Meta:
        db_table = 'medico'

    def __str__(self):
        return self.usuario.first_name