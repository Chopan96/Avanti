from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from ..utils.utils import validar_rut, normalizar_y_validar_rut  # Asegúrate de que la ruta sea correcta

class CustomUserManager(BaseUserManager):
    def create_user(self, rut, email, password=None, **extra_fields):
        """Crea y devuelve un usuario con rut, email y password."""
        if not rut:
            raise ValueError('El RUT debe ser proporcionado')

        # Validar y normalizar el RUT
        rut_normalizado = normalizar_y_validar_rut(rut)
        if not rut_normalizado:
            raise ValueError('El RUT proporcionado no es válido')

        email = self.normalize_email(email)
        user = self.model(rut=rut_normalizado, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, rut, email, password=None, **extra_fields):
        """Crea y devuelve un superusuario."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if not extra_fields.get('is_staff'):
            raise ValueError('El superusuario debe tener is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(rut, email, password, **extra_fields)


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

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para validar y normalizar el RUT
        antes de guardar el usuario.
        """
        # Validar y normalizar el RUT
        rut_normalizado = normalizar_y_validar_rut(self.rut)
        if not rut_normalizado:
            raise ValueError(f"El RUT {self.rut} no es válido.")
        self.rut = rut_normalizado
        super().save(*args, **kwargs)  # Llama al método save original
