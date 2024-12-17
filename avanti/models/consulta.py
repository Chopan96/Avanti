from django.db import models

class Consulta(models.Model):
    fecha_consulta = models.DateField()
    motivo = models.TextField()
    observaciones = models.TextField()
    ficha_clinica = models.ForeignKey('FichaClinica', on_delete=models.CASCADE, related_name='consultas')
    medico = models.ForeignKey('Medico', on_delete=models.SET_NULL, null=True, blank=True, related_name='consultas')  # Relación con Medico


    def __str__(self):
        return f"Consulta {self.fecha_consulta} - {self.ficha_clinica.paciente.usuario.first_name}"
