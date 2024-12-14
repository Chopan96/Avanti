from django.db import models

class Historial(models.Model):
    ficha_clinica = models.ForeignKey('FichaClinica', on_delete=models.CASCADE, related_name='historiales')
    consulta = models.ForeignKey('Consulta', on_delete=models.CASCADE, related_name='historiales')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Historial del paciente {self.ficha_clinica.paciente.nombre} - Consulta {self.consulta.fecha_consulta}"
