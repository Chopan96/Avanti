import unittest
from ..utils.utils import calcular_dv, validar_rut, normalizar_y_validar_rut

class TestRutFunctions(unittest.TestCase):

    def test_calcular_dv(self):
        """
        Pruebas para verificar que el cálculo del dígito verificador es correcto.
        """
        test_cases = [
            ("19430788", "8"),
            ("10953507", "9"),
            ("21229239", "7"),
        ]
        for cuerpo, expected_dv in test_cases:
            with self.subTest(cuerpo=cuerpo, expected_dv=expected_dv):
                self.assertEqual(calcular_dv(cuerpo), expected_dv)

    def test_validar_rut(self):
        """
        Pruebas para verificar que la validación de RUT es correcta.
        """
        valid_ruts = [
            "194307888",
            "109535079",
            "212292397",
        ]
        invalid_ruts = [
            "32132138-5",  # DV incorrecto
            "22222222-1",  # DV incorrecto
            "00000000-0",  # Cuerpo fuera de rango
            "999999999-9", # Cuerpo fuera de rango
            "abcdefg",     # No numérico
            "123",         # Largo insuficiente
        ]
        for rut in valid_ruts:
            with self.subTest(rut=rut):
                self.assertTrue(validar_rut(rut))
        
        for rut in invalid_ruts:
            with self.subTest(rut=rut):
                self.assertFalse(validar_rut(rut))

    def test_normalizar_y_validar_rut(self):
        """
        Pruebas para verificar que la normalización y validación combinadas funcionan correctamente.
        """
        test_cases = [
            ("212292397","21.229.239-7"),
            ("194307888","19.430.788-8"),
            ("109535079","10.953.507-9"),
        ]
        invalid_cases = [
            "22333555-5",  # DV incorrecto
            "abcdefg",     # No numérico
            "123",         # Largo insuficiente
        ]

        for rut, expected in test_cases:
            with self.subTest(rut=rut):
                self.assertEqual(normalizar_y_validar_rut(rut), expected)

        for rut in invalid_cases:
            with self.subTest(rut=rut):
                self.assertIsNone(normalizar_y_validar_rut(rut))

if __name__ == "__main__":
    unittest.main()
