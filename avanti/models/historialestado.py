


from django.db import models

class HistorialEstado(models.Model):
    historialestado = models.CharField(primary_key=True, max_length=20)
    fechacambio = models.DateField(blank=True, null=True)
    estado = models.ForeignKey('Estado', models.CASCADE, db_column='id_estado')
    cita = models.ForeignKey('Cita', models.CASCADE, db_column='id_cita')
    prevision = models.ForeignKey(
        'Prevision', models.CASCADE, db_column='prevision', to_field='prevision', related_name='historialestado_prevision_set'
    )
    paciente_rut = models.ForeignKey(
        'Paciente', models.CASCADE, db_column='paciente_rut', to_field='rut', related_name='historialestado_paciente_set'
    )

    class Meta:
        db_table = 'historial_estado'
        constraints = [
            models.UniqueConstraint(
                fields=['historialestado', 'estado', 'cita', 'prevision', 'paciente_rut'],
                name='unique_historialestado'
            )
        ]

