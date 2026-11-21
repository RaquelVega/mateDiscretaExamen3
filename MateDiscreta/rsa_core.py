"""
Lógica central de encriptación y desencriptación RSA con validaciones completas.
Proyecto de Criptografía RSA - MM2015 Matemática Discreta 1

Integrantes:
- Raquel Pamela Tejada Vega (Carné: 25469)
- José Carlos Argueta González (Carné: 25652)
Herramientas de apoyo:
- Depuración y revisión de código asistida por Antigravity (Gemini 3.8 Flash)
"""

from typing import Any, Dict, List
from rsa_math import es_primo, mcd, inverso_modular, exponenciacion_modular


class ValidacionError(Exception):
    """Excepción personalizada para errores de validación de datos y parámetros."""
    pass


def validar_parametros_rsa(p: Any, q: Any, e: Any) -> tuple[int, int, int, int, int]:
    """
    Valida los parámetros RSA p, q, e según las condiciones del proyecto:
    1. p, q y e deben ser enteros.
    2. p y q deben ser números primos distintos.
    3. n = p * q debe satisfacer: 126126 < n < 1000000.
    4. phi = (p - 1) * (q - 1).
    5. e > 1 y MCD(e, phi) == 1.
    
    Retorna:
        tuple[int, int, int, int, int]: (p, q, e, n, phi)
    """
    # 1. Validación de tipos enteros
    try:
        p_int = int(p)
        q_int = int(q)
        e_int = int(e)
    except (ValueError, TypeError):
        raise ValidacionError("Los parámetros p, q y e deben ser números enteros válidos.")
    
    # 2. Primalidad de p y q
    if not es_primo(p_int):
        raise ValidacionError(f"El valor p = {p_int} no es un número primo.")
    if not es_primo(q_int):
        raise ValidacionError(f"El valor q = {q_int} no es un número primo.")
    if p_int == q_int:
        raise ValidacionError(f"Los primos p y q deben ser distintos (se ingresó {p_int} en ambos).")
    
    # 3. Cálculo de n y phi
    n = p_int * q_int
    phi = (p_int - 1) * (q_int - 1)
    
    if not (126126 < n < 1000000):
        raise ValidacionError(
            f"El módulo n = p * q = {n} no está en el rango permitido (126126 < n < 1000000)."
        )
    
    # 4. Validación de e
    if e_int <= 1:
        raise ValidacionError(f"El exponente público e = {e_int} debe ser estrictamente mayor que 1.")
    
    comun_divisor = mcd(e_int, phi)
    if comun_divisor != 1:
        raise ValidacionError(
            f"El exponente e = {e_int} no es coprimo con φ = {phi} (MCD({e_int}, {phi}) = {comun_divisor})."
        )
    
    return p_int, q_int, e_int, n, phi


def validar_mensaje(mensaje: str) -> None:
    """
    Verifica que cada carácter del mensaje tenga código ASCII entre 32 y 126.
    No sustituye ni elimina caracteres automáticamente.
    
    Lanza:
        ValidacionError si el mensaje está vacío o contiene caracteres inválidos.
    """
    if mensaje is None or len(mensaje) == 0:
        raise ValidacionError("El mensaje a encriptar no puede estar vacío.")
    
    caracteres_invalidos = []
    for idx, c in enumerate(mensaje):
        codigo = ord(c)
        if codigo < 32 or codigo > 126:
            caracteres_invalidos.append((idx + 1, repr(c), codigo))
            
    if caracteres_invalidos:
        detalles = ", ".join(
            [f"'{char}' (ASCII {cod}) en posición {pos}" for pos, char, cod in caracteres_invalidos[:5]]
        )
        if len(caracteres_invalidos) > 5:
            detalles += f" ... y {len(caracteres_invalidos) - 5} más"
        raise ValidacionError(
            f"El mensaje contiene {len(caracteres_invalidos)} carácter(es) fuera del rango ASCII [32, 126]: {detalles}. "
            f"No se admiten tildes, ñ, tabulaciones ni saltos de línea."
        )


def encriptar(mensaje: str, p: Any, q: Any, e: Any) -> Dict[str, Any]:
    """
    Ejecuta el proceso completo de encriptación RSA según las especificaciones.
    
    Pasos:
    1. Validar mensaje M y parámetros p, q, e. Registrar longitud original L.
    2. Si L es impar, agregar un espacio al final (código 032).
    3. Separar en parejas y formar bloques numéricos m de 6 dígitos.
    4. Calcular c = (m^e) mod n mediante exponenciación modular propia.
    5. Formatear cada c con exactamente 6 dígitos.
    
    Retorna:
        Dict con los resultados y el detalle paso a paso para la interfaz.
    """
    validar_mensaje(mensaje)
    p_val, q_val, e_val, n, phi = validar_parametros_rsa(p, q, e)
    
    L = len(mensaje)
    tuvo_relleno = (L % 2 != 0)
    
    if tuvo_relleno:
        mensaje_procesado = mensaje + " "
    else:
        mensaje_procesado = mensaje
        
    bloques_detalle = []
    bloques_cifrados = []
    
    # Procesar de 2 en 2 caracteres
    num_parejas = len(mensaje_procesado) // 2
    for i in range(num_parejas):
        c1 = mensaje_procesado[2 * i]
        c2 = mensaje_procesado[2 * i + 1]
        
        asc1 = ord(c1)
        asc2 = ord(c2)
        
        asc1_str = f"{asc1:03d}"
        asc2_str = f"{asc2:03d}"
        
        bloque_m_str = asc1_str + asc2_str
        bloque_m_int = int(bloque_m_str)
        
        # Cifrado con exponenciación modular propia
        bloque_c_int = exponenciacion_modular(bloque_m_int, e_val, n)
        bloque_c_str = f"{bloque_c_int:06d}"
        
        bloques_cifrados.append(bloque_c_str)
        bloques_detalle.append({
            "indice": i + 1,
            "par_caracteres": (c1, c2),
            "texto_par": f"'{c1}''{c2}'",
            "ascii_par": f"{asc1_str} {asc2_str}",
            "m_num": bloque_m_int,
            "m_str": bloque_m_str,
            "c_num": bloque_c_int,
            "c_str": bloque_c_str,
            "es_relleno": (tuvo_relleno and i == num_parejas - 1)
        })
        
    cifrado_completo = " ".join(bloques_cifrados)
    
    return {
        "p": p_val,
        "q": q_val,
        "e": e_val,
        "n": n,
        "phi": phi,
        "mensaje_original": mensaje,
        "mensaje_procesado": mensaje_procesado,
        "L": L,
        "tuvo_relleno": tuvo_relleno,
        "bloques_cifrados": bloques_cifrados,
        "cifrado_completo": cifrado_completo,
        "llave_publica": (e_val, n),
        "bloques_detalle": bloques_detalle
    }


def desencriptar(cifrado_str: str, L_val: Any, p: Any, q: Any, e: Any) -> Dict[str, Any]:
    """
    Ejecuta el proceso completo de desencriptación RSA según las especificaciones.
    
    Pasos:
    1. Validar p, q, e; calcular n y phi. Validar formato de C y coherencia con L.
    2. Calcular inverso modular d de e módulo phi (1 <= d < phi).
    3. Para cada bloque cifrado c, recuperar m = (c^d) mod n mediante exp. modular.
    4. Escribir cada m con 6 dígitos, dividir en 2 códigos de 3 dígitos y validar rango [32, 126].
    5. Si L es impar, comprobar que el último carácter sea espacio y retirarlo exactamente.
    
    Retorna:
        Dict con los resultados y el detalle paso a paso para la interfaz.
    """
    p_val, q_val, e_val, n, phi = validar_parametros_rsa(p, q, e)
    
    if cifrado_str is None or not cifrado_str.strip():
        raise ValidacionError("El texto cifrado C no puede estar vacío.")
    
    # Validar bloques de C
    bloques_raw = cifrado_str.strip().split()
    k = len(bloques_raw)
    if k == 0:
        raise ValidacionError("No se encontraron bloques cifrados válidos en C.")
    
    bloques_c_int = []
    for idx, bloque in enumerate(bloques_raw, 1):
        if len(bloque) != 6 or not bloque.isdigit():
            raise ValidacionError(
                f"El bloque {idx} ('{bloque}') es inválido. "
                f"Cada bloque cifrado debe tener exactamente 6 dígitos decimales (0-9)."
            )
        val = int(bloque)
        if not (0 <= val < n):
            raise ValidacionError(
                f"El bloque {idx} con valor {val} está fuera de rango. Debe satisfacer 0 <= c < n ({n})."
            )
        bloques_c_int.append(val)
        
    # Validar longitud L
    try:
        L = int(L_val)
    except (ValueError, TypeError):
        raise ValidacionError(f"La longitud original L ('{L_val}') debe ser un número entero.")
    
    if L <= 0:
        raise ValidacionError(f"La longitud original L ({L}) debe ser mayor que cero.")
    
    # Coherencia de L con la cantidad de bloques k: L debe ser 2*k o 2*k - 1
    if L != 2 * k and L != (2 * k - 1):
        raise ValidacionError(
            f"Incoherencia entre la longitud L={L} y la cantidad de bloques cifrados k={k}. "
            f"Para k={k} bloques, L solo puede ser {2 * k} (sin relleno) o {2 * k - 1} (con relleno)."
        )
        
    tuvo_relleno = (L % 2 != 0)
    
    # Calcular clave privada d
    d = inverso_modular(e_val, phi)
    
    bloques_detalle = []
    caracteres_recuperados = []
    
    for idx, c_val in enumerate(bloques_c_int, 1):
        # Exponenciación modular propia: m = (c^d) mod n
        m_val = exponenciacion_modular(c_val, d, n)
        m_str = f"{m_val:06d}"
        
        code1_str = m_str[0:3]
        code2_str = m_str[3:6]
        
        code1 = int(code1_str)
        code2 = int(code2_str)
        
        if not (32 <= code1 <= 126):
            raise ValidacionError(
                f"En el bloque {idx}, el primer código recuperado ({code1:03d}) "
                f"está fuera del rango ASCII imprimible [032, 126]."
            )
        if not (32 <= code2 <= 126):
            raise ValidacionError(
                f"En el bloque {idx}, el segundo código recuperado ({code2:03d}) "
                f"está fuera del rango ASCII imprimible [032, 126]."
            )
            
        char1 = chr(code1)
        char2 = chr(code2)
        
        caracteres_recuperados.append(char1)
        caracteres_recuperados.append(char2)
        
        bloques_detalle.append({
            "indice": idx,
            "c_str": f"{c_val:06d}",
            "c_num": c_val,
            "m_num": m_val,
            "m_str": m_str,
            "ascii_par": f"{code1_str} {code2_str}",
            "par_caracteres": (char1, char2),
            "texto_par": f"'{char1}''{char2}'",
            "es_relleno": (tuvo_relleno and idx == k)
        })
        
    texto_completo = "".join(caracteres_recuperados)
    
    # Manejo exacto del relleno según especificación
    if tuvo_relleno:
        ultimo_caracter = texto_completo[-1]
        if ultimo_caracter != " ":
            raise ValidacionError(
                f"Se especificó L={L} impar (con relleno), pero el último carácter "
                f"recuperado no es un espacio (se obtuvo ASCII {ord(ultimo_caracter)})."
            )
        # Retirar exactamente el último carácter
        mensaje_final = texto_completo[:-1]
    else:
        mensaje_final = texto_completo
        
    return {
        "p": p_val,
        "q": q_val,
        "e": e_val,
        "n": n,
        "phi": phi,
        "d": d,
        "L": L,
        "tuvo_relleno": tuvo_relleno,
        "llave_privada": (d, n),
        "llave_publica": (e_val, n),
        "cifrado_original": cifrado_str,
        "mensaje_recuperado": mensaje_final,
        "texto_con_posible_relleno": texto_completo,
        "bloques_detalle": bloques_detalle
    }
