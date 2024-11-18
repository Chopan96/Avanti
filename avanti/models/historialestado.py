


from django.db import models

class HistorialEstado(models.Model):
    id_historialestado = models.CharField(primary_key=True, max_length=20)
    fechacambio = models.DateField(blank=True, null=True)
    id_estado = models.ForeignKey('Estado', models.CASCADE, db_column='id_estado')
    id_cita = models.ForeignKey('Cita', models.CASCADE, db_column='id_cita')
    id_prevision = models.ForeignKey(
        'Prevision', models.CASCADE, db_column='id_prevision', to_field='id_prevision', related_name='historialestado_prevision_set'
    )
    paciente_rut = models.ForeignKey(
        'Paciente', models.CASCADE, db_column='paciente_rut', to_field='rut', related_name='historialestado_paciente_set'
    )

    class Meta:
        db_table = 'historial_estado'
        constraints = [
            models.UniqueConstraint(
                fields=['id_historialestado', 'id_estado', 'id_cita', 'id_prevision', 'paciente_rut'],
                name='unique_historialestado'
            )
        ]

