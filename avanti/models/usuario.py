from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, rut, email, password=None, **extra_fields):
        """Crea y devuelve un usuario con rut, email y password."""
        if not rut:
            raise ValueError('El rut debe ser proporcionado')
        email = self.normalize_email(email)
        user = self.model(rut=rut, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, rut, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if not extra_fields.get('is_staff'):
            raise ValueError('El superusuario debe tener is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return Usuario.objects.create_user(rut, email, password, **extra_fields)


class Usuario(AbstractUser):
    rut = models.CharField(max_length=12, unique=True)  # Usamos rut como identificador único
    fono = models.BigIntegerField(blank=True, null=True)
    
    # Elimina el campo 'username' de la autenticación
    username = None

    # Usa 'rut' como el campo único para la autenticación
    USERNAME_FIELD = 'rut'
    REQUIRED_FIELDS = ['email']  # Agrega cualquier otro campo que quieras como obligatorio

    objects = CustomUserManager()

    def __str__(self):
        return self.rut

    # Sobrescribe el método create_superuser para usar rut en lugar de username
    def create_superuser(self, rut, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(rut, email, password, **extra_fields)
