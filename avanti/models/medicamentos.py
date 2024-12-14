from django.db import models

class Medicamento(models.Model):
    consulta = models.ForeignKey('Consulta', related_name='medicamentos', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"Medicamento en consulta {self.consulta.fecha_consulta}"
