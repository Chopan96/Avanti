import random
import string
import re

def generar_password_temporal(length=12):
    """
    Genera una contraseña temporal de forma aleatoria.
    Combina letras mayúsculas, minúsculas, dígitos y caracteres especiales.
    """
    caracteres = string.ascii_letters + string.digits + "!@#$%^&*()-_"
    return ''.join(random.choices(caracteres, k=length))

def normalizar_rut(rut):
    """
    Normaliza el RUT eliminando puntos, guiones y formatea al estilo '12.345.678-9'.
    """
    if not rut:
        return None

    # Eliminar puntos y guiones
    rut = re.sub(r'[^0-9kK]', '', rut)

    # Validar que tenga al menos cuerpo y dígito verificador
    if len(rut) < 2:
        return None

    cuerpo, dv = rut[:-1], rut[-1].upper()
    # Formatear el cuerpo con puntos
    cuerpo_formateado = f"{int(cuerpo):,}".replace(",", ".")
    return f"{cuerpo_formateado}-{dv}"
