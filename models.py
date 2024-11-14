# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Administrativo(models.Model):
    rut = models.OneToOneField('Usuario', models.DO_NOTHING, db_column='rut', primary_key=True)
    cargo = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'administrativo'


class Alergias(models.Model):
    id_alergias = models.CharField(primary_key=True, max_length=20)
    descripcion = models.TextField(blank=True, null=True)
    id_historial = models.ForeignKey('Historial', models.DO_NOTHING, db_column='id_historial')

    class Meta:
        managed = False
        db_table = 'alergias'


class Bono(models.Model):
    id_bono = models.CharField(primary_key=True, max_length=20)  # The composite primary key (id_bono, id_reporte, administrativo_rut) found, that is not supported. The first column is selected.
    monto = models.BigIntegerField(blank=True, null=True)
    feccreacion = models.DateField(blank=True, null=True)
    fecvigencia = models.DateField(blank=True, null=True)
    id_cita = models.ForeignKey('Cita', models.DO_NOTHING, db_column='id_cita')
    paciente_rut = models.ForeignKey('Cita', models.DO_NOTHING, db_column='paciente_rut', to_field='paciente_rut', related_name='bono_paciente_rut_set')
    id_prevision = models.ForeignKey('Cita', models.DO_NOTHING, db_column='id_prevision', to_field='id_prevision', related_name='bono_id_prevision_set')
    id_reporte = models.ForeignKey('Reportes', models.DO_NOTHING, db_column='id_reporte')
    administrativo_rut = models.ForeignKey('Reportes', models.DO_NOTHING, db_column='administrativo_rut', to_field='administrativo_rut', related_name='bono_administrativo_rut_set')

    class Meta:
        managed = False
        db_table = 'bono'
        unique_together = (('id_bono', 'id_reporte', 'administrativo_rut'), ('id_cita', 'paciente_rut', 'id_prevision'),)


class Cita(models.Model):
    id_cita = models.CharField(primary_key=True, max_length=20)  # The composite primary key (id_cita, paciente_rut, id_prevision) found, that is not supported. The first column is selected.
    hora = models.DateField(blank=True, null=True)
    id_prevision = models.ForeignKey('Prevision', models.DO_NOTHING, db_column='id_prevision')
    id_sala = models.ForeignKey('Horario', models.DO_NOTHING, db_column='id_sala', to_field='id_sala')
    medico_rut = models.ForeignKey('Horario', models.DO_NOTHING, db_column='medico_rut', related_name='cita_medico_rut_set')
    paciente_rut = models.ForeignKey('Paciente', models.DO_NOTHING, db_column='paciente_rut')

    class Meta:
        managed = False
        db_table = 'cita'
        unique_together = (('id_cita', 'paciente_rut', 'id_prevision'), ('medico_rut', 'id_sala'),)


class Diagnosticos(models.Model):
    id_diagnostico = models.CharField(primary_key=True, max_length=20)  # The composite primary key (id_diagnostico, id_historial) found, that is not supported. The first column is selected.
    descripcion = models.TextField(blank=True, null=True)
    id_historial = models.ForeignKey('Historial', models.DO_NOTHING, db_column='id_historial')

    class Meta:
        managed = False
        db_table = 'diagnosticos'
        unique_together = (('id_diagnostico', 'id_historial'),)


class Disponibilidad(models.Model):
    fecha = models.DateField(blank=True, null=True)
    horainicio = models.DateField(blank=True, null=True)
    horafin = models.DateField(blank=True, null=True)
    medico_rut = models.OneToOneField('Medico', models.DO_NOTHING, db_column='medico_rut', primary_key=True)

    class Meta:
        managed = False
        db_table = 'disponibilidad'


class EnfermedadesBase(models.Model):
    id_enfbase = models.CharField(primary_key=True, max_length=20)
    descripcion = models.TextField(blank=True, null=True)
    id_historial = models.ForeignKey('Historial', models.DO_NOTHING, db_column='id_historial')

    class Meta:
        managed = False
        db_table = 'enfermedades_base'


class Estado(models.Model):
    id_estado = models.CharField(primary_key=True, max_length=12)
    descripcion = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estado'


class Historial(models.Model):
    id_historial = models.CharField(primary_key=True, max_length=20)
    edad = models.BigIntegerField(blank=True, null=True)
    paciente_rut = models.OneToOneField('Paciente', models.DO_NOTHING, db_column='paciente_rut')

    class Meta:
        managed = False
        db_table = 'historial'


class HistorialEstado(models.Model):
    id_historialestado = models.CharField(primary_key=True, max_length=20)  # The composite primary key (id_historialestado, id_estado, id_cita, id_prevision, paciente_rut) found, that is not supported. The first column is selected.
    fechacambio = models.DateField(blank=True, null=True)
    id_estado = models.ForeignKey(Estado, models.DO_NOTHING, db_column='id_estado')
    id_cita = models.ForeignKey(Cita, models.DO_NOTHING, db_column='id_cita')
    id_prevision = models.ForeignKey(Cita, models.DO_NOTHING, db_column='id_prevision', to_field='id_prevision', related_name='historialestado_id_prevision_set')
    paciente_rut = models.ForeignKey(Cita, models.DO_NOTHING, db_column='paciente_rut', to_field='paciente_rut', related_name='historialestado_paciente_rut_set')

    class Meta:
        managed = False
        db_table = 'historial_estado'
        unique_together = (('id_historialestado', 'id_estado', 'id_cita', 'id_prevision', 'paciente_rut'),)


class Horario(models.Model):
    fecha = models.DateField(blank=True, null=True)
    horainicio = models.DateField(blank=True, null=True)
    horafin = models.DateField(blank=True, null=True)
    id_sala = models.ForeignKey('Sala', models.DO_NOTHING, db_column='id_sala')
    medico_rut = models.OneToOneField(Disponibilidad, models.DO_NOTHING, db_column='medico_rut', primary_key=True)  # The composite primary key (medico_rut, id_sala) found, that is not supported. The first column is selected.

    class Meta:
        managed = False
        db_table = 'horario'
        unique_together = (('medico_rut', 'id_sala'),)


class Medicamentos(models.Model):
    id_medicamentos = models.CharField(primary_key=True, max_length=20)  # The composite primary key (id_medicamentos, id_historial) found, that is not supported. The first column is selected.
    nombre = models.TextField(blank=True, null=True)
    id_historial = models.ForeignKey(Historial, models.DO_NOTHING, db_column='id_historial')

    class Meta:
        managed = False
        db_table = 'medicamentos'
        unique_together = (('id_medicamentos', 'id_historial'),)


class Medico(models.Model):
    rut = models.OneToOneField('Usuario', models.DO_NOTHING, db_column='rut', primary_key=True)
    especialidad = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'medico'


class MetodoDePago(models.Model):
    id_metodo = models.CharField(primary_key=True, max_length=20)
    tipo = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'metodo_de_pago'


class Paciente(models.Model):
    rut = models.OneToOneField('Usuario', models.DO_NOTHING, db_column='rut', primary_key=True)

    class Meta:
        managed = False
        db_table = 'paciente'


class Pago(models.Model):
    id_pago = models.CharField(primary_key=True, max_length=20)  # The composite primary key (id_pago, id_bono, id_reporte, administrativo_rut, id_metodo) found, that is not supported. The first column is selected.
    monto = models.BigIntegerField(blank=True, null=True)
    fechapago = models.DateField(blank=True, null=True)
    id_bono = models.ForeignKey(Bono, models.DO_NOTHING, db_column='id_bono')
    id_metodo = models.ForeignKey(MetodoDePago, models.DO_NOTHING, db_column='id_metodo')
    id_reporte = models.ForeignKey(Bono, models.DO_NOTHING, db_column='id_reporte', to_field='id_reporte', related_name='pago_id_reporte_set')
    administrativo_rut = models.ForeignKey(Bono, models.DO_NOTHING, db_column='administrativo_rut', to_field='administrativo_rut', related_name='pago_administrativo_rut_set')

    class Meta:
        managed = False
        db_table = 'pago'
        unique_together = (('id_pago', 'id_bono', 'id_reporte', 'administrativo_rut', 'id_metodo'),)


class Prevision(models.Model):
    id_prevision = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    tipo = models.CharField(max_length=50, blank=True, null=True)
    cobertura = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prevision'


class Reportes(models.Model):
    id_reporte = models.CharField(primary_key=True, max_length=20)  # The composite primary key (id_reporte, administrativo_rut) found, that is not supported. The first column is selected.
    fechainicio = models.DateField(blank=True, null=True)
    fechafin = models.DateField(blank=True, null=True)
    ingresos = models.BigIntegerField(blank=True, null=True)
    total = models.BigIntegerField(blank=True, null=True)
    administrativo_rut = models.ForeignKey(Administrativo, models.DO_NOTHING, db_column='administrativo_rut')

    class Meta:
        managed = False
        db_table = 'reportes'
        unique_together = (('id_reporte', 'administrativo_rut'),)


class Sala(models.Model):
    id_sala = models.CharField(primary_key=True, max_length=12)
    numero = models.BigIntegerField(blank=True, null=True)
    capacidad = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sala'


class Usuario(models.Model):
    rut = models.CharField(primary_key=True, max_length=12)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    apellido = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    permisos = models.CharField(max_length=50, blank=True, null=True)
    fono = models.BigIntegerField(blank=True, null=True)
    mail = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario'
