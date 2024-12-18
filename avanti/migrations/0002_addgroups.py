from django.db import migrations

def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    # Crear grupos
    paciente_group, _ = Group.objects.get_or_create(name='Paciente')
    medico_group, _ = Group.objects.get_or_create(name='Medico')
    padmin_group, _ = Group.objects.get_or_create(name='Personal Administrativo')

    # Crear los ContentTypes y permisos para el modelo 'Consulta' (relacionado con el médico)
    consulta_ct = ContentType.objects.get(app_label='avanti', model='consulta')
    consulta_view = Permission.objects.get(codename='view_consulta', content_type=consulta_ct)
    consulta_add = Permission.objects.get(codename='add_consulta', content_type=consulta_ct)
    consulta_change = Permission.objects.get(codename='change_consulta', content_type=consulta_ct)
    consulta_delete = Permission.objects.get(codename='delete_consulta', content_type=consulta_ct)

    # Crear permisos para otros modelos
    fichaclinica_ct = ContentType.objects.get(app_label='avanti', model='fichaclinica')
    fichaclinica_view = Permission.objects.get(codename='view_fichaclinica', content_type=fichaclinica_ct)
    fichaclinica_add = Permission.objects.get(codename='add_fichaclinica', content_type=fichaclinica_ct)
    fichaclinica_change = Permission.objects.get(codename='change_fichaclinica', content_type=fichaclinica_ct)
    fichaclinica_delete= Permission.objects.get(codename='delete_fichaclinica', content_type=fichaclinica_ct)

    alergia_ct = ContentType.objects.get(app_label='avanti', model='alergia')
    alergia_view = Permission.objects.get(codename='view_alergia', content_type=alergia_ct)
    alergia_add = Permission.objects.get(codename='add_alergia', content_type=alergia_ct)
    alergia_change = Permission.objects.get(codename='change_alergia', content_type=alergia_ct)
    alergia_delete= Permission.objects.get(codename='delete_alergia', content_type=alergia_ct)

    diagnostico_ct = ContentType.objects.get(app_label='avanti', model='diagnostico')
    diagnostico_view = Permission.objects.get(codename='view_diagnostico', content_type=diagnostico_ct)
    diagnostico_add = Permission.objects.get(codename='add_diagnostico', content_type=diagnostico_ct)
    diagnostico_change = Permission.objects.get(codename='change_diagnostico', content_type=diagnostico_ct)
    diagnostico_delete= Permission.objects.get(codename='delete_diagnostico', content_type=diagnostico_ct)

    enfermedadesbase_ct = ContentType.objects.get(app_label='avanti', model='enfermedadesbase')
    enfermedadesbase_view = Permission.objects.get(codename='view_enfermedadesbase', content_type=enfermedadesbase_ct)
    enfermedadesbase_add = Permission.objects.get(codename='add_enfermedadesbase', content_type=enfermedadesbase_ct)
    enfermedadesbase_change = Permission.objects.get(codename='change_enfermedadesbase', content_type=enfermedadesbase_ct)
    enfermedadesbase_delete= Permission.objects.get(codename='delete_enfermedadesbase', content_type=enfermedadesbase_ct)

    medicamento_ct = ContentType.objects.get(app_label='avanti', model='medicamento')
    medicamento_view = Permission.objects.get(codename='view_medicamento', content_type=medicamento_ct)
    medicamento_add = Permission.objects.get(codename='add_medicamento', content_type=medicamento_ct)
    medicamento_change = Permission.objects.get(codename='change_medicamento', content_type=medicamento_ct)
    medicamento_delete= Permission.objects.get(codename='delete_medicamento', content_type=medicamento_ct)

    disponibilidad_ct = ContentType.objects.get(app_label='avanti', model='disponibilidad')
    disponibilidad_view = Permission.objects.get(codename='view_disponibilidad', content_type=disponibilidad_ct)
    disponibilidad_add = Permission.objects.get(codename='add_disponibilidad', content_type=disponibilidad_ct)
    disponibilidad_change = Permission.objects.get(codename='change_disponibilidad', content_type=disponibilidad_ct)
    disponibilidad_delete= Permission.objects.get(codename='delete_disponibilidad', content_type=disponibilidad_ct)

    horario_ct = ContentType.objects.get(app_label='avanti', model='horario')
    horario_view = Permission.objects.get(codename='view_horario', content_type=horario_ct)
    horario_add = Permission.objects.get(codename='add_horario', content_type=horario_ct)
    horario_change = Permission.objects.get(codename='change_horario', content_type=horario_ct)
    horario_delete= Permission.objects.get(codename='delete_horario', content_type=horario_ct)

    cita_ct = ContentType.objects.get(app_label='avanti', model='cita')
    cita_view = Permission.objects.get(codename='view_cita', content_type=cita_ct)
    cita_add = Permission.objects.get(codename='add_cita', content_type=cita_ct)
    cita_change = Permission.objects.get(codename='change_cita', content_type=cita_ct)
    cita_delete= Permission.objects.get(codename='delete_cita', content_type=cita_ct)

    sala_ct = ContentType.objects.get(app_label='avanti', model='sala')
    sala_view = Permission.objects.get(codename='view_sala', content_type=sala_ct)
    sala_add = Permission.objects.get(codename='add_sala', content_type=sala_ct)
    sala_change = Permission.objects.get(codename='change_sala', content_type=sala_ct)
    sala_delete= Permission.objects.get(codename='delete_sala', content_type=sala_ct)

    bono_ct = ContentType.objects.get(app_label='avanti', model='bono')
    bono_view = Permission.objects.get(codename='view_bono', content_type=bono_ct)
    bono_add = Permission.objects.get(codename='add_bono', content_type=bono_ct)
    bono_change = Permission.objects.get(codename='change_bono', content_type=bono_ct)
    bono_delete= Permission.objects.get(codename='delete_bono', content_type=bono_ct)

    reportes_ct = ContentType.objects.get(app_label='avanti', model='reportes')
    reportes_view = Permission.objects.get(codename='view_reportes', content_type=reportes_ct)
    reportes_add = Permission.objects.get(codename='add_reportes', content_type=reportes_ct)
    reportes_change = Permission.objects.get(codename='change_reportes', content_type=reportes_ct)
    reportes_delete= Permission.objects.get(codename='delete_reportes', content_type=reportes_ct)

    pago_ct = ContentType.objects.get(app_label='avanti', model='pago')
    pago_view = Permission.objects.get(codename='view_pago', content_type=pago_ct)
    pago_add = Permission.objects.get(codename='add_pago', content_type=pago_ct)
    pago_change = Permission.objects.get(codename='change_pago', content_type=pago_ct)
    pago_delete= Permission.objects.get(codename='delete_pago', content_type=pago_ct)

    # Asignar permisos a los grupos
    medico_group.permissions.add(
        consulta_view, consulta_add, consulta_change, consulta_delete,
        fichaclinica_view, fichaclinica_add, fichaclinica_change, fichaclinica_delete,
        alergia_view, alergia_delete, alergia_add, alergia_change,
        diagnostico_add, diagnostico_change, diagnostico_view, diagnostico_delete,
        enfermedadesbase_add, enfermedadesbase_delete, enfermedadesbase_change, enfermedadesbase_view,
        medicamento_add, medicamento_change, medicamento_view, medicamento_delete,
        horario_view, horario_change, cita_view, cita_change,
    )

    padmin_group.permissions.add(
        horario_change, horario_add, horario_view, horario_delete,
        disponibilidad_add, disponibilidad_change, disponibilidad_view, disponibilidad_delete,
        cita_view, sala_add, sala_change, sala_view, sala_delete,
        pago_add, pago_change, pago_delete, pago_view, bono_add,
        bono_change, bono_delete, bono_view, reportes_add,
        reportes_change, reportes_delete, reportes_view,
    )

    paciente_group.permissions.add(
        cita_add, cita_change, cita_view, cita_delete, bono_view,
        fichaclinica_view, alergia_view, diagnostico_view, enfermedadesbase_view,
        medicamento_view, horario_view, pago_view
    )

class Migration(migrations.Migration):

    dependencies = [
        ('avanti', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]