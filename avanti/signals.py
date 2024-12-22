from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Usuario, Paciente, Medico, Administrativo,Especialidad

@receiver(m2m_changed, sender=Usuario.groups.through)
def crear_perfil_grupo(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":  # Solo actúa después de asignar un grupo
        print(f"Se detectó un cambio en los grupos del usuario: {instance.rut}")
        for group_pk in pk_set:  # Revisa cada grupo asignado
            grupo = Group.objects.get(pk=group_pk)
            if grupo.name == "Personal Administrativo":
                Administrativo.objects.get_or_create(usuario=instance, defaults={"cargo": "No especificado"})
                print("Perfil de Personal Administrativo creado.")
            elif grupo.name == "Medico":
                # Buscar o crear la especialidad "General"
                especialidad, created = Especialidad.objects.get_or_create(nombre="General")
                Medico.objects.get_or_create(usuario=instance, defaults={"especialidad": especialidad})
                print("Perfil de Médico creado.")
            elif grupo.name == "Paciente":
                Paciente.objects.get_or_create(usuario=instance, defaults={"direccion": "No especificada"})
                print("Perfil de Paciente creado.")
