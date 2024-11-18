from django.db import models

class Administrativo(models.Model):
    rut = models.OneToOneField('Usuario', on_delete=models.CASCADE, db_column='rut', primary_key=True)
    cargo = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'administrativo'