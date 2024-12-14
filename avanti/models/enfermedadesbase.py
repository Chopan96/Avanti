from django.db import models

class EnfermedadesBase(models.Model):
    consulta = models.ForeignKey('Consulta', related_name='enfermedades_base', on_delete=models.CASCADE)
    descripcion = models.TextField()

    def __str__(self):
        return f"Enfermedad Base en consulta {self.consulta.fecha_consulta}"