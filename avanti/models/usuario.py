from django.db import models


class Usuario(models.Model):
    rut = models.CharField(primary_key=True, max_length=12)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    apellido = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    permisos = models.CharField(max_length=50, blank=True, null=True)
    fono = models.BigIntegerField(blank=True, null=True)
    mail = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = 'usuario'
        
    def __str__(self):
        return f"{self.nombre} - {self.rut}"

