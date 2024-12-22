from django.contrib.auth.backends import ModelBackend
from .utils import normalizar_y_validar_rut  # Asegúrate de importar correctamente tu función
from ..models import Usuario  # Importa tu modelo personalizado

import logging
logger = logging.getLogger(__name__)

class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        logger.debug(f"Intentando autenticar con username (RUT): {username}")
        if username is None or password is None:
            logger.debug("Username (RUT) o contraseña no proporcionados")
            return None

        # Normaliza el "username" como si fuera un RUT
        rut_normalizado = normalizar_y_validar_rut(username)
        if not rut_normalizado:
            logger.debug("El RUT proporcionado no es válido")
            return None

        try:
            # Busca al usuario usando el RUT normalizado
            user = Usuario.objects.get(rut=rut_normalizado)
            if user.check_password(password):
                logger.debug("Autenticación exitosa")
                return user
            logger.debug("Contraseña incorrecta")
        except Usuario.DoesNotExist:
            logger.debug("Usuario no encontrado")
        return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            logger.debug(f"Usuario con ID {user_id} no encontrado")
            return None
