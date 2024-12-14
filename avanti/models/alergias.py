from django.db import models

class Alergia(models.Model):
    consulta = models.ForeignKey('Consulta', related_name='alergias', on_delete=models.CASCADE)
    descripcion = models.TextField()

    def __str__(self):
        return f"Alergia en consulta {self.consulta.fecha_consulta}"