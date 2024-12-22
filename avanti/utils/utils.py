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

def calcular_dv(rut):
    """
    Calcula el dígito verificador de un RUT chileno con mensajes de depuración.
    """
    # Convertir el RUT a string para procesarlo
    rut = str(rut)
    print(f"[DEBUG] Calculando DV para RUT: {rut}")

    # Revertir los dígitos del RUT
    rut_reverso = rut[::-1]
    print(f"[DEBUG] RUT reverso: {rut_reverso}")

    # Serie de multiplicadores (2, 3, 4, 5, 6, 7 repetido)
    serie = [2, 3, 4, 5, 6, 7]

    # Calcular la suma ponderada
    suma = 0
    for i, digito in enumerate(rut_reverso):
        ponderacion = int(digito) * serie[i % len(serie)]
        suma += ponderacion
        print(f"[DEBUG] Dígito: {digito}, Ponderación: {ponderacion}, Suma acumulada: {suma}")

    # Calcular el módulo 11
    resto = suma % 11
    print(f"[DEBUG] Suma total: {suma}, Resto módulo 11: {resto}")

    # Obtener el dígito verificador
    dv = 11 - resto
    if dv == 11:
        print(f"[DEBUG] DV calculado: 0")
        return "0"
    elif dv == 10:
        print(f"[DEBUG] DV calculado: K")
        return "K"
    else:
        print(f"[DEBUG] DV calculado: {dv}")
        return str(dv)




def validar_rut(rut):
    """
    Valida si un RUT chileno es correcto con mensajes de depuración.
    """
    print(f"[DEBUG] Validando RUT: {rut}")

    if not rut:
        print("[DEBUG] RUT vacío o nulo.")
        return False

    # Eliminar puntos y guiones
    rut = re.sub(r'[^0-9kK]', '', rut)
    print(f"[DEBUG] RUT sin formato: {rut}")

    # Validar que tenga al menos 2 caracteres (cuerpo + DV)
    if len(rut) < 2:
        print("[DEBUG] RUT demasiado corto.")
        return False

    # Separar cuerpo y dígito verificador
    cuerpo, dv = rut[:-1], rut[-1].upper()
    print(f"[DEBUG] Cuerpo: {cuerpo}, DV: {dv}")

    # Validar que el cuerpo sea numérico
    if not cuerpo.isdigit():
        print("[DEBUG] El cuerpo del RUT no es numérico.")
        return False

    # Validar que el cuerpo esté en el rango válido
    cuerpo_num = int(cuerpo)
    if cuerpo_num < 1000000 or cuerpo_num > 99999999:
        print(f"[DEBUG] Cuerpo fuera de rango: {cuerpo_num}")
        return False

    # Validar que el dígito verificador sea válido (número o 'K')
    if dv not in "0123456789K":
        print(f"[DEBUG] DV inválido: {dv}")
        return False

    # Calcular DV esperado y comparar
    dv_calculado = calcular_dv(cuerpo)
    print(f"[DEBUG] DV esperado: {dv_calculado}, DV proporcionado: {dv}")
    return dv_calculado == dv




def normalizar_y_validar_rut(rut):
    """
    Valida y normaliza un RUT chileno con mensajes de depuración.
    """
    print(f"[DEBUG] Normalizando y validando RUT: {rut}")

    if not validar_rut(rut):
        print(f"[DEBUG] RUT inválido: {rut}")
        return None

    # Eliminar puntos y guiones
    rut = re.sub(r'[^0-9kK]', '', rut)
    print(f"[DEBUG] RUT sin formato después de validar: {rut}")

    # Separar cuerpo y dígito verificador
    cuerpo, dv = rut[:-1], rut[-1].upper()

    # Formatear el cuerpo con puntos
    cuerpo_formateado = f"{int(cuerpo):,}".replace(",", ".")
    rut_normalizado = f"{cuerpo_formateado}-{dv}"
    print(f"[DEBUG] RUT normalizado: {rut_normalizado}")
    return rut_normalizado





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
