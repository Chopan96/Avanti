from django.db import models

class Administrativo(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE, primary_key=True, related_name='perfil_administrativo')
    cargo = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'administrativo'