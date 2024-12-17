import random
import string

def generar_password_temporal(length=12):
    """
    Genera una contraseña temporal de forma aleatoria.
    Combina letras mayúsculas, minúsculas, dígitos y caracteres especiales.
    """
    caracteres = string.ascii_letters + string.digits + "!@#$%^&*()-_"
    return ''.join(random.choices(caracteres, k=length))
