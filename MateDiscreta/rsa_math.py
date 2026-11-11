"""
Módulo de algoritmos matemáticos propios para RSA.
Proyecto de Criptografía RSA - MM2015 Matemática Discreta 1

Integrantes:
- Raquel Pamela Tejada Vega (Carné: 25469)
- José Carlos Argueta González (Carné: 25652)
- Asistente de IA: Antigravity (Google DeepMind - Gemini 3.8 Flash)

Restricciones académicas cumplidas:
- No se utiliza math.gcd ni bibliotecas de criptografía.
- No se utiliza pow() con módulo ni pow(e, -1, phi).
- No se calcula la potencia completa antes del módulo.
- Exponenciación modular propia con reducciones sucesivas módulo n.
- Algoritmo de Euclides propio para el MCD.
- Algoritmo Extendido de Euclides propio para el inverso modular.
- Comprobación propia de primalidad.
"""


def es_primo(num: int) -> bool:
    """
    Comprueba si un número entero es primo utilizando el método de divisiones
    por tentativa optimizado (paso 6k +/- 1).
    
    Parámetros:
        num (int): Número a evaluar.
        
    Retorna:
        bool: True si num es primo, False en caso contrario.
    """
    if not isinstance(num, int):
        return False
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    
    # Comprobar divisores impares de la forma 6k +/- 1 hasta sqrt(num)
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True


def mcd(a: int, b: int) -> int:
    """
    Calcula el Máximo Común Divisor entre dos enteros a y b mediante
    el Algoritmo de Euclides clásico por divisiones sucesivas.
    
    Parámetros:
        a (int): Primer número.
        b (int): Segundo número.
        
    Retorna:
        int: MCD(a, b) >= 0.
    """
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("Los argumentos del MCD deben ser enteros.")
    
    a = abs(a)
    b = abs(b)
    
    while b != 0:
        residuo = a % b
        a = b
        b = residuo
    return a


def euclides_extendido(a: int, b: int) -> tuple[int, int, int]:
    """
    Implementación iterativa del Algoritmo Extendido de Euclides.
    Calcula el MCD(a, b) y los coeficientes de Bézout (x, y) tales que:
        a * x + b * y = mcd(a, b)
        
    Parámetros:
        a (int): Primer entero.
        b (int): Segundo entero.
        
    Retorna:
        tuple[int, int, int]: (g, x, y) donde g = mcd(a, b).
    """
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    
    temp_a, temp_b = a, b
    
    while temp_b != 0:
        cociente = temp_a // temp_b
        temp_a, temp_b = temp_b, temp_a % temp_b
        x0, x1 = x1, x0 - cociente * x1
        y0, y1 = y1, y0 - cociente * y1
        
    return temp_a, x0, y0


def inverso_modular(e: int, phi: int) -> int:
    """
    Calcula el inverso modular de e módulo phi, es decir, el entero d tal que:
        e * d = 1 (mod phi) con 1 <= d < phi.
        
    Utiliza el Algoritmo Extendido de Euclides propio sin utilizar pow(e, -1, phi).
    
    Parámetros:
        e (int): Exponente público.
        phi (int): Valor de la función de Euler phi(n).
        
    Retorna:
        int: Exponente privado d en el rango [1, phi - 1].
        
    Lanza:
        ValueError: Si e y phi no son coprimos (MCD(e, phi) != 1) o si phi <= 1.
    """
    if phi <= 1:
        raise ValueError(f"El módulo phi ({phi}) debe ser mayor que 1.")
    
    g, x, _ = euclides_extendido(e, phi)
    if g != 1:
        raise ValueError(
            f"El exponente e={e} no tiene inverso modular módulo phi={phi} "
            f"porque MCD({e}, {phi}) = {g} != 1."
        )
    
    # Ajustar x para obtener el representante en el intervalo [1, phi - 1]
    d = x % phi
    if d < 1:
        d += phi
    return d


def exponenciacion_modular(base: int, exp: int, mod: int) -> int:
    """
    Calcula (base^exp) mod mod mediante el método binario (Square-and-Multiply)
    reduciendo módulo mod en cada multiplicación intermedia.
    
    Cumple estrictamente con la especificación de NO calcular la potencia
    completa ni utilizar pow(base, exp, mod) nativo.
    
    Parámetros:
        base (int): Base entera.
        exp (int): Exponente entero no negativo.
        mod (int): Módulo entero mayor que 1.
        
    Retorna:
        int: Resultado en el rango 0 <= resultado < mod.
    """
    if mod <= 1:
        raise ValueError(f"El módulo ({mod}) debe ser estrictamente mayor que 1.")
    if exp < 0:
        raise ValueError(f"El exponente ({exp}) debe ser un entero no negativo.")
    
    resultado = 1
    base = base % mod
    
    potencia_actual = exp
    while potencia_actual > 0:
        # Si el bit actual es 1, multiplicamos y reducimos
        if potencia_actual % 2 == 1:
            resultado = (resultado * base) % mod
        # Elevamos al cuadrado la base y reducimos módulo mod
        base = (base * base) % mod
        potencia_actual //= 2
        
    return resultado
