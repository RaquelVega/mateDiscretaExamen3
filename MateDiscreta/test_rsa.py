"""
Suite de pruebas unitarias para el sistema de criptografía RSA.
Proyecto MM2015 Matemática Discreta 1

Integrantes:
- Raquel Pamela Tejada Vega (Carné: 25469)
- José Carlos Argueta González (Carné: 25652)
- Herramientas de apoyo:Depuración y revisión de código asistida por Antigravity (Gemini 3.8 Flash)
"""

import unittest
from rsa_math import es_primo, mcd, euclides_extendido, inverso_modular, exponenciacion_modular
from rsa_core import validar_parametros_rsa, validar_mensaje, encriptar, desencriptar, ValidacionError


class TestRsaMath(unittest.TestCase):
    """Pruebas para las funciones matemáticas en rsa_math.py."""

    def test_es_primo(self):
        # Números no primos
        self.assertFalse(es_primo(-7))
        self.assertFalse(es_primo(0))
        self.assertFalse(es_primo(1))
        self.assertFalse(es_primo(4))
        self.assertFalse(es_primo(9))
        self.assertFalse(es_primo(100))
        self.assertFalse(es_primo(367 * 373))
        
        # Números primos
        self.assertTrue(es_primo(2))
        self.assertTrue(es_primo(3))
        self.assertTrue(es_primo(5))
        self.assertTrue(es_primo(7))
        self.assertTrue(es_primo(17))
        self.assertTrue(es_primo(367))
        self.assertTrue(es_primo(373))
        self.assertTrue(es_primo(997))

    def test_mcd(self):
        self.assertEqual(mcd(54, 24), 6)
        self.assertEqual(mcd(17, 136152), 1)
        self.assertEqual(mcd(100, 10), 10)
        self.assertEqual(mcd(0, 5), 5)
        self.assertEqual(mcd(7, 0), 7)
        self.assertEqual(mcd(-15, 20), 5)

    def test_inverso_modular(self):
        # Caso del enunciado: e = 17, phi = 136152 -> d = 8009
        d = inverso_modular(17, 136152)
        self.assertEqual(d, 8009)
        self.assertEqual((17 * d) % 136152, 1)
        self.assertTrue(1 <= d < 136152)

        # Inverso con números pequeños
        # 3 * d = 1 (mod 11) -> 3 * 4 = 12 = 1 (mod 11) -> d = 4
        self.assertEqual(inverso_modular(3, 11), 4)

        # Error si no son coprimos
        with self.assertRaises(ValueError):
            inverso_modular(6, 15)

    def test_exponenciacion_modular(self):
        # 2^10 mod 1000 = 1024 mod 1000 = 24
        self.assertEqual(exponenciacion_modular(2, 10, 1000), 24)
        # 5^0 mod 13 = 1
        self.assertEqual(exponenciacion_modular(5, 0, 13), 1)
        # Caso de referencia: m = 82083, e = 17, n = 136891 -> c = 26054
        self.assertEqual(exponenciacion_modular(82083, 17, 136891), 26054)
        # Desencriptado: c = 26054, d = 8009, n = 136891 -> m = 82083
        self.assertEqual(exponenciacion_modular(26054, 8009, 136891), 82083)


class TestRsaReferenceExample(unittest.TestCase):
    """Verificación exacta del caso de referencia oficial de la guía."""

    def test_caso_guia_rsa(self):
        # Datos del enunciado:
        # Mensaje: "RSA"
        # p = 367, q = 373, e = 17
        res_enc = encriptar("RSA", 367, 373, 17)
        
        # Validar salidas esperadas
        self.assertEqual(res_enc["n"], 136891)
        self.assertEqual(res_enc["phi"], 136152)
        self.assertEqual(res_enc["L"], 3)
        self.assertTrue(res_enc["tuvo_relleno"])
        self.assertEqual(res_enc["mensaje_procesado"], "RSA ")
        
        # Bloques del mensaje numéricos esperados
        self.assertEqual(res_enc["bloques_detalle"][0]["m_str"], "082083")
        self.assertEqual(res_enc["bloques_detalle"][1]["m_str"], "065032")
        
        # Cifrado esperado: 026054 123875 (comprueba el cero inicial en 026054)
        self.assertEqual(res_enc["bloques_cifrados"], ["026054", "123875"])
        self.assertEqual(res_enc["cifrado_completo"], "026054 123875")
        
        # Desencriptación
        res_dec = desencriptar(
            cifrado_str=res_enc["cifrado_completo"],
            L_val=3,
            p=367,
            q=373,
            e=17
        )
        
        self.assertEqual(res_dec["d"], 8009)
        self.assertEqual(res_dec["mensaje_recuperado"], "RSA")


class TestRsaCasosFuncionamiento(unittest.TestCase):
    """
    Comprobaciones requeridas por el enunciado:
    - Longitud par e impar.
    - Mayúsculas y minúsculas.
    - Números y signos.
    - Espacios consecutivos.
    - Espacios originales al inicio y al final.
    - Ceros iniciales en bloques cifrados.
    """

    def setUp(self):
        # Primos válidos que generan n en rango:
        # p = 367, q = 373 -> n = 136891 (126126 < n < 1000000)
        self.p = 367
        self.q = 373
        self.e = 17

    def _roundtrip(self, mensaje_original):
        enc = encriptar(mensaje_original, self.p, self.q, self.e)
        dec = desencriptar(enc["cifrado_completo"], enc["L"], self.p, self.q, self.e)
        self.assertEqual(dec["mensaje_recuperado"], mensaje_original)
        self.assertEqual(len(dec["mensaje_recuperado"]), len(mensaje_original))
        return enc, dec

    def test_longitud_par(self):
        msg = "HOLA"  # 4 caracteres (par, sin relleno)
        enc, dec = self._roundtrip(msg)
        self.assertFalse(enc["tuvo_relleno"])
        self.assertEqual(enc["L"], 4)

    def test_longitud_impar(self):
        msg = "HOLA!"  # 5 caracteres (impar, con relleno)
        enc, dec = self._roundtrip(msg)
        self.assertTrue(enc["tuvo_relleno"])
        self.assertEqual(enc["L"], 5)

    def test_mayusculas_y_minusculas(self):
        msg = "Criptografia RSA y Matematica Discreta"
        self._roundtrip(msg)

    def test_numeros_y_signos(self):
        msg = "Cod: 25469 & 25652; Val = $100 + [40% - 15*2]!"
        self._roundtrip(msg)

    def test_espacios_consecutivos(self):
        msg = "Uno   dos      tres   cuatro"
        self._roundtrip(msg)

    def test_espacios_inicio_y_final_impar(self):
        msg = "   Mensaje con espacios al inicio y fin   "  # 42 chars (par) + 1 = 43 chars
        msg_impar = msg + "X"
        self._roundtrip(msg_impar)

    def test_espacios_inicio_y_final_par(self):
        msg = "  Texto con espacios  "
        self._roundtrip(msg)

    def test_un_solo_caracter(self):
        msg = "Z"
        enc, dec = self._roundtrip(msg)
        self.assertEqual(enc["L"], 1)
        self.assertTrue(enc["tuvo_relleno"])


class TestRsaValidacionesErrores(unittest.TestCase):
    """
    Comprobaciones del rechazo de datos inválidos requeridas por el enunciado:
    - Parámetros RSA inválidos (p, q no primos, p=q, n fuera de rango, e no coprimo).
    - Caracteres no admitidos (tildes, ñ, saltos de línea).
    - Bloques mal formados (longitudes distintas de 6, caracteres no numéricos).
    - Valores cifrados fuera de rango (c >= n).
    - Longitudes L inconsistentes con la cantidad de bloques.
    """

    def test_p_o_q_no_primo(self):
        # p = 368 (par, no primo)
        with self.assertRaises(ValidacionError) as ctx:
            encriptar("Test", 368, 373, 17)
        self.assertIn("no es un número primo", str(ctx.exception))

    def test_p_y_q_iguales(self):
        with self.assertRaises(ValidacionError) as ctx:
            encriptar("Test", 367, 367, 17)
        self.assertIn("deben ser distintos", str(ctx.exception))

    def test_n_fuera_de_rango_inferior(self):
        # Primos pequeños: 101 * 103 = 10403 < 126126
        with self.assertRaises(ValidacionError) as ctx:
            encriptar("Test", 101, 103, 17)
        self.assertIn("rango permitido", str(ctx.exception))

    def test_n_fuera_de_rango_superior(self):
        # Primos grandes: 1009 * 1013 = 1022117 > 1000000
        with self.assertRaises(ValidacionError) as ctx:
            encriptar("Test", 1009, 1013, 17)
        self.assertIn("rango permitido", str(ctx.exception))

    def test_e_no_coprimo_con_phi(self):
        # p=367, q=373 -> phi = 136152. 136152 es divisible por 2, 3, etc.
        # Si elegimos e = 6, MCD(6, 136152) != 1
        with self.assertRaises(ValidacionError) as ctx:
            encriptar("Test", 367, 373, 6)
        self.assertIn("no es coprimo con φ", str(ctx.exception))

    def test_e_menor_o_igual_a_uno(self):
        with self.assertRaises(ValidacionError) as ctx:
            encriptar("Test", 367, 373, 1)
        self.assertIn("mayor que 1", str(ctx.exception))

    def test_mensaje_con_tildes_o_caracteres_no_ascii(self):
        # Caracteres no admitidos: 'ñ', 'ó', etc.
        with self.assertRaises(ValidacionError) as ctx:
            validar_mensaje("Criptografía")
        self.assertIn("fuera del rango ASCII", str(ctx.exception))

    def test_mensaje_con_saltos_de_linea(self):
        with self.assertRaises(ValidacionError) as ctx:
            validar_mensaje("Linea 1\nLinea 2")
        self.assertIn("fuera del rango ASCII", str(ctx.exception))

    def test_cifrado_bloque_mal_formado_longitud(self):
        # Bloque de 5 dígitos en vez de 6
        with self.assertRaises(ValidacionError) as ctx:
            desencriptar("02605 123875", 3, 367, 373, 17)
        self.assertIn("debe tener exactamente 6 dígitos", str(ctx.exception))

    def test_cifrado_bloque_mal_formado_no_numerico(self):
        with self.assertRaises(ValidacionError) as ctx:
            desencriptar("02605A 123875", 3, 367, 373, 17)
        self.assertIn("debe tener exactamente 6 dígitos", str(ctx.exception))

    def test_cifrado_bloque_fuera_de_rango_modulo(self):
        # n = 136891. Un bloque con 136892 >= n
        with self.assertRaises(ValidacionError) as ctx:
            desencriptar("136892 123875", 3, 367, 373, 17)
        self.assertIn("fuera de rango", str(ctx.exception))

    def test_longitud_incoherente_con_bloques(self):
        # k = 2 bloques -> L solo puede ser 3 o 4. Si se pone L = 1 o L = 5 debe fallar.
        with self.assertRaises(ValidacionError) as ctx:
            desencriptar("026054 123875", 5, 367, 373, 17)
        self.assertIn("Incoherencia entre la longitud L", str(ctx.exception))

        with self.assertRaises(ValidacionError) as ctx:
            desencriptar("026054 123875", 2, 367, 373, 17)
        self.assertIn("Incoherencia entre la longitud L", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
