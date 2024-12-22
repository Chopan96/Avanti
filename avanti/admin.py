from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Paciente, Medico, Administrativo, Sala, Sucursal, Prevision, Especialidad

class CustomUserAdmin(UserAdmin):
    # Campos para la vista de detalle del usuario
    fieldsets = (
        (None, {'fields': ('rut', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'email', 'fono')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    # Campos para el formulario de creación de usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('rut', 'email', 'password1', 'password2', 'first_name', 'last_name', 'fono', 'groups'),
        }),
    )

    list_display = ('rut', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('rut', 'email', 'first_name', 'last_name')
    ordering = ('rut',)

    

# Registra el modelo de usuario personalizado
admin.site.register(Usuario, CustomUserAdmin)

# Registra los otros modelos
admin.site.register(Paciente)
admin.site.register(Medico)
admin.site.register(Administrativo)
admin.site.register(Sala)
admin.site.register(Sucursal)
admin.site.register(Prevision)
admin.site.register(Especialidad)
