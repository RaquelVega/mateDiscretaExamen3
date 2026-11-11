# Proyecto de Criptografía RSA
**Curso:** MM2015 Matemática Discreta 1  
**Universidad del Valle de Guatemala**  

---

## 👥 Integrantes y Asistencia de IA

- **Raquel Pamela Tejada Vega** — Carné: `25469`
- **José Carlos Argueta González** — Carné: `25652`
- **Asistente de Inteligencia Artificial:** Antigravity (Google DeepMind — Gemini 3.8 Flash)

---

## 🎥 Video Demostrativo

- **Enlace de revisión:** `[Pegar aquí el enlace al video demostrativo]`

---

## 📌 Descripción del Proyecto

Aplicación con interfaz gráfica en Python que implementa el criptosistema asimétrico RSA para encriptar y desencriptar mensajes de texto respetando los principios de la aritmética modular y la teoría de números.

### Cumplimiento estricto de restricciones matemáticas
- **Sin funciones sustitutas de biblioteca:** No se utiliza `math.gcd`, `pow` modular de 3 argumentos, `pow(e, -1, phi)` ni módulos criptográficos externos.
- **Sin potencias gigantes:** No se calcula la potencia entera completa antes del módulo; el cómputo se realiza reduciendo módulo $n$ en cada paso.
- **Algoritmos propios desarrollados:**
  1. Comprobación de primalidad por divisiones por tentativa optimizadas ($6k \pm 1$).
  2. Máximo Común Divisor mediante el Algoritmo de Euclides.
  3. Inverso modular mediante el Algoritmo Extendido de Euclides.
  4. Exponenciación modular mediante el método binario (*Square-and-Multiply*).

---

## 💻 Entorno y Requisitos de Ejecución

- **Versión de Python:** Python 3.10 o superior (verificado en Python 3.13).
- **Dependencias externas:** **Ninguna**. El proyecto se diseñó utilizando exclusivamente la **biblioteca estándar de Python** (`tkinter`, `ttk`, `unittest`, `typing`, `sys`). No requiere instalación de paquetes vía `pip`.

### Instrucciones de ejecución

1. **Iniciar la aplicación gráfica:**
   ```bash
   python main.py
   ```
   *(También puede iniciarse directamente con `python gui.py`)*.

2. **Ejecutar la suite de pruebas automatizadas:**
   ```bash
   python -m unittest test_rsa.py -v
   ```

---

## 📂 Organización de Archivos y Funciones Matemáticas

| Archivo | Función / Algoritmo | Descripción y Propósito |
|---|---|---|
| [`rsa_math.py`](file:///c:/Users/Angy/MateDiscreta/rsa_math.py) | `es_primo(num)` | Verifica si un entero es primo para validar $p$ y $q$. |
| [`rsa_math.py`](file:///c:/Users/Angy/MateDiscreta/rsa_math.py) | `mcd(a, b)` | Algoritmo de Euclides. Valida que $\operatorname{MCD}(e, \varphi) = 1$. |
| [`rsa_math.py`](file:///c:/Users/Angy/MateDiscreta/rsa_math.py) | `inverso_modular(e, phi)`<br>`euclides_extendido(a, b)` | Algoritmo Extendido de Euclides. Obtiene el exponente privado $d$ tal que $e \cdot d \equiv 1 \pmod \varphi$ con $1 \le d < \varphi$. |
| [`rsa_math.py`](file:///c:/Users/Angy/MateDiscreta/rsa_math.py) | `exponenciacion_modular(base, exp, mod)` | Exponenciación binaria con reducción modular paso a paso para cifrar ($c \equiv m^e \pmod n$) y descifrar ($m \equiv c^d \pmod n$). |
| [`rsa_core.py`](file:///c:/Users/Angy/MateDiscreta/rsa_core.py) | `validar_parametros_rsa`<br>`validar_mensaje`<br>`encriptar`<br>`desencriptar` | Lógica de validación, codificación ASCII [32, 126], empaquetado de bloques en 6 dígitos y gestión del relleno. |
| [`gui.py`](file:///c:/Users/Angy/MateDiscreta/gui.py) | `RSAApplication` | Interfaz gráfica interactiva (Tkinter/ttk) con paneles de detalle, tablas de bloques y validación visual. |
| [`main.py`](file:///c:/Users/Angy/MateDiscreta/main.py) | `main()` | Punto de arranque del sistema. |
| [`test_rsa.py`](file:///c:/Users/Angy/MateDiscreta/test_rsa.py) | `TestRsa...` | Suite de 25 pruebas unitarias automatizadas. |
| [`requirements.txt`](file:///c:/Users/Angy/MateDiscreta/requirements.txt) | Documentación de dependencias | Especifica el uso de la biblioteca estándar de Python. |

---

## 🔄 Uso de las Operaciones

### 1. Encriptación
1. Ingrese los números primos distintos $p$ y $q$, y el exponente público $e$ (o presione el botón *"Cargar Ejemplo de Guía"*).
2. Escriba el mensaje original $M$ en el campo de texto (se admiten caracteres ASCII entre 32 y 126: mayúsculas, minúsculas, espacios y símbolos).
3. Presione el botón **Encriptar**.
4. La aplicación calcula y presenta:
   - Resumen matemático: $n$, $\varphi$, verificación de $\operatorname{MCD}(e, \varphi) = 1$, llave pública $(e, n)$ y longitud $L$.
   - Cifrado $C$ y estado del relleno.
   - Tabla detallada con cada bloque: pareja de caracteres, códigos ASCII de 3 dígitos, bloque numérico $m$, operación modular y bloque cifrado resultante $c$ en 6 dígitos.

### 2. Desencriptación
1. Ingrese los parámetros $p$, $q$ y $e$.
2. Pegue o ingrese el mensaje cifrado $C$ (bloques de 6 dígitos separados por espacios).
3. Ingrese el valor entero de la longitud original $L$.
4. Presione el botón **Desencriptar**.
5. La aplicación calcula el exponente privado $d$, recupera cada bloque numérico $m \equiv c^d \pmod n$, decodifica los códigos ASCII, gestiona el relleno y restaura el mensaje original exacto $M$.

*(Nota: En la interfaz se dispone del botón "Transferir C y L a Desencriptar" para agilizar las pruebas entre pestañas).*

---

## 🔑 Ubicación de $C$ y $L$, Ingreso en Desencriptación y Mecanismo de Relleno

### ¿Dónde se muestran $C$ y $L$?
- Al encriptar, el **Cifrado $C$** aparece en el panel derecho en un campo de texto destacado de solo lectura con opción de copia directa.
- La **Longitud original $L$** se visualiza inmediatamente debajo de $C$, junto con el conteo de bloques generados y la indicación de si hubo o no relleno.

### ¿Cómo ingresarlos al desencriptar?
- En la pestaña de desencriptación se tienen campos dedicados:
  - **Cifrado C:** Campo de texto donde se colocan los bloques numéricos separados por espacios. Cada bloque debe tener exactamente 6 dígitos decimales y cumplir $0 \le c < n$.
  - **Longitud original L:** Campo donde se ingresa el entero $L$. El sistema valida que para $k$ bloques, $L$ sea estrictamente igual a $2k$ (caso par, sin relleno) o a $2k - 1$ (caso impar, con relleno). Cualquier inconsistencia genera un mensaje de error descriptivo sin cerrar el programa.

### ¿Cómo funciona el relleno (*Padding*)?
- Cada bloque numérico procesa parejas de dos caracteres ASCII.
- Si la longitud original $L$ es **impar**, al final del mensaje se agrega **exactamente un espacio** (código ASCII `032`) como carácter de relleno antes de formar los bloques.
- Durante la desencriptación:
  - Si $L$ es **impar**, se comprueba que el último carácter obtenido sea efectivamente un espacio y se retira **únicamente** ese carácter (`texto[:-1]`).
  - Si $L$ es **par**, **no se retira ningún carácter**.
- **Preservación de espacios originales:** En ningún momento se emplea `.strip()` ni eliminación indiscriminada de espacios, asegurando que los espacios originales al inicio, en medio o al final del texto se conserven exactamente.

---

## 📊 Ejemplo Completo de Referencia

Verificación paso a paso del caso presentado en las especificaciones del proyecto:

| Parámetro / Etapa | Valor Obtenido | Detalle |
|---|---|---|
| **Mensaje original $M$** | `"RSA"` | Longitud original $L = 3$ |
| **Entradas RSA** | $p = 367$, $q = 373$, $e = 17$ | $p$ y $q$ primos distintos |
| **Módulo $n$** | $136891$ | $n = 367 \times 373$ ($126126 < n < 1000000$) |
| **Función $\varphi$** | $136152$ | $\varphi = 366 \times 372$ |
| **Coprimidad** | $\operatorname{MCD}(17, 136152) = 1$ | Exponente válido ($e > 1$) |
| **Relleno** | $L = 3$ (impar) $\to$ `"RSA "` | Se añade 1 espacio ASCII `032` al final |
| **Bloque 1** | `'R'` (082), `'S'` (083) | $m_1 = 082083 \implies c_1 \equiv 82083^{17} \pmod{136891} =$ **`026054`** |
| **Bloque 2** | `'A'` (065), `' '` (032) | $m_2 = 065032 \implies c_2 \equiv 65032^{17} \pmod{136891} =$ **`123875`** |
| **Cifrado $C$** | `026054 123875` | 2 bloques de 6 dígitos (cero inicial conservado) |
| **Exponente privado $d$** | $8009$ | $17 \cdot 8009 \equiv 1 \pmod{136152}$ con $1 \le d < 136152$ |
| **Descifrado de bloques** | $m_1 = 26054^{8009} \pmod n = 82083$<br>$m_2 = 123875^{8009} \pmod n = 65032$ | Códigos ASCII: $082, 083 \to$ `"RS"`<br>Códigos ASCII: $065, 032 \to$ `"A "` |
| **Ajuste por relleno** | Último carácter = `' '` verificado | Se retira el espacio de relleno |
| **Mensaje recuperado** | `"RSA"` | Coincidencia exacta con el mensaje original |

---

## 🧪 Comprobaciones y Pruebas Realizadas

La suite de pruebas automatizadas (`test_rsa.py`) incluye 25 casos de prueba unitarios organizados en tres categorías:

1. **Pruebas de Algoritmos Matemáticos:**
   - Primalidad (`es_primo`): números compuestos, pares, primos pequeños y primos de 3 dígitos.
   - Algoritmo de Euclides (`mcd`): números coprimos, múltiplos y divisores comunes.
   - Inverso modular (`inverso_modular`): obtención de $d$, verificación de $e \cdot d \equiv 1 \pmod \varphi$ y rechazo de no coprimos.
   - Exponenciación modular (`exponenciacion_modular`): propiedades de potencias y cálculo modular correcto con enteros grandes.

2. **Pruebas de Casos Válidos del Criptosistema:**
   - Recuperación exacta del caso de referencia `"RSA"` ($L=3$, ceros a la izquierda en bloques cifrados).
   - Mensajes con longitud par (sin relleno) e impar (con relleno).
   - Textos con mayúsculas, minúsculas, números y signos de puntuación.
   - Textos con espacios consecutivos.
   - Textos con espacios originales al inicio y al final (comprobando que no se truncan).

3. **Pruebas de Validación y Rechazo de Errores:**
   - Rechazo de parámetros $p$ o $q$ no primos o repetidos ($p = q$).
   - Rechazo de $n$ fuera del rango permitido ($n \le 126126$ o $n \ge 1000000$).
   - Rechazo de $e \le 1$ o que no sea coprimo con $\varphi$.
   - Rechazo de caracteres no admitidos (tildes, `ñ`, saltos de línea `\n`, tabulaciones).
   - Rechazo de bloques cifrados mal formados (longitud distinta de 6 o caracteres no numéricos).
   - Rechazo de bloques cifrados fuera de rango ($c \ge n$).
   - Rechazo de longitudes $L$ inconsistentes con el número de bloques $k$.
