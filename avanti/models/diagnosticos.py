from django.db import models

class Diagnostico(models.Model):
    consulta = models.ForeignKey('Consulta', related_name='diagnosticos', on_delete=models.CASCADE)
    descripcion = models.TextField()

    def __str__(self):
        return f"Diagnóstico en consulta {self.consulta.fecha_consulta}"
