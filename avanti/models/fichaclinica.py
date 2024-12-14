from django.db import models

class FichaClinica(models.Model):
    paciente = models.OneToOneField('Paciente', on_delete=models.CASCADE)
    edad = models.IntegerField()  # Edad directamente en la ficha clínica
    fecha_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Ficha Clínica de {self.paciente.usuario.first_name}"