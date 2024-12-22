from django.db import migrations

def cargar_datos(apps, schema_editor):
    # Obtiene los modelos desde apps para asegurar compatibilidad con migraciones.
    Sucursal = apps.get_model('avanti', 'Sucursal')
    Sala = apps.get_model('avanti', 'Sala')
    Prevision = apps.get_model('avanti', 'Prevision')
    Especialidad = apps.get_model('avanti', 'Especialidad')

    # Cargar datos en Sucursal
    sucursales = [
        {'sucursal': 'S001', 'nombre': 'Sucursal Central', 'direccion': 'Av. Principal 123, Ciudad'},
        {'sucursal': 'S002', 'nombre': 'Sucursal Norte', 'direccion': 'Calle Norte 456, Ciudad'},
        {'sucursal': 'S003', 'nombre': 'Sucursal Sur', 'direccion': 'Av. Sur 789, Ciudad'}
    ]
    for sucursal_data in sucursales:
        Sucursal.objects.create(**sucursal_data)

    # Cargar datos en Sala
    salas = [
        {'sala': 'R001', 'numero': 101, 'capacidad': 10, 'sucursal_id': 'S001'},
        {'sala': 'R002', 'numero': 102, 'capacidad': 20, 'sucursal_id': 'S001'},
        {'sala': 'R003', 'numero': 201, 'capacidad': 15, 'sucursal_id': 'S002'}
    ]
    for sala_data in salas:
        Sala.objects.create(**sala_data)

    # Cargar datos en Prevision
    previsiones = [
        {'prevision': 'P001', 'nombre': 'Fonasa', 'tipo': 'Pública', 'cobertura': '100% en hospitales públicos'},
        {'prevision': 'P002', 'nombre': 'Isapre Vida', 'tipo': 'Privada', 'cobertura': '80% en consultas y hospitales'},
    ]
    for prevision_data in previsiones:
        Prevision.objects.create(**prevision_data)

    # Cargar datos en Especialidad
    especialidades = [
        {'nombre': 'Cardiología'},
        {'nombre': 'Pediatría'},
        {'nombre': 'Dermatología'},
        {'nombre': 'Ginecología'},
        {'nombre': 'Neurología'}
    ]
    for especialidad_data in especialidades:
        Especialidad.objects.create(**especialidad_data)

def revertir_datos(apps, schema_editor):
    # Obtiene los modelos desde apps
    Sucursal = apps.get_model('avanti', 'Sucursal')
    Sala = apps.get_model('avanti', 'Sala')
    Prevision = apps.get_model('avanti', 'Prevision')
    Especialidad = apps.get_model('avanti', 'Especialidad')

    # Borra los datos cargados
    Sucursal.objects.all().delete()
    Sala.objects.all().delete()
    Prevision.objects.all().delete()
    Especialidad.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('avanti', '0002_addgroups'),
    ]

    operations = [
        migrations.RunPython(cargar_datos, revertir_datos),
    ]
