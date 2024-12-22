from django.db import models

class Especialidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'especialidad'
        verbose_name = 'Especialidad'
        verbose_name_plural = 'Especialidades'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
