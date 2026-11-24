import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from narrar.ptbr import cardinal, normalize_ptbr  # noqa: E402


class NumberTests(unittest.TestCase):
    def test_cardinals_used_in_speech(self):
        self.assertEqual(cardinal(0), "zero")
        self.assertEqual(cardinal(15), "quinze")
        self.assertEqual(cardinal(21), "vinte e um")
        self.assertEqual(cardinal(100), "cem")
        self.assertEqual(cardinal(101), "cento e um")
        self.assertEqual(cardinal(1000), "mil")
        self.assertEqual(cardinal(1100), "mil e cem")
        self.assertEqual(cardinal(1101), "mil cento e um")
        self.assertEqual(cardinal(2000), "dois mil")
        self.assertEqual(cardinal(2001), "dois mil e um")
        self.assertEqual(cardinal(2025), "dois mil e vinte e cinco")
        self.assertEqual(cardinal(2500), "dois mil e quinhentos")
        self.assertEqual(cardinal(1_000_000), "um milhão")
        self.assertEqual(cardinal(2_000_001), "dois milhões e um")


class NormalizeTests(unittest.TestCase):
    def test_abbreviations(self):
        self.assertEqual(normalize_ptbr("Dr. Pedro e a Dra. Ana falaram com o Sr. Lima."), "doutor Pedro e a doutora Ana falaram com o senhor Lima.")
        self.assertIn("etcétera.", normalize_ptbr("Trouxe exemplos, etc."))
        self.assertIn("por exemplo", normalize_ptbr("Veja p.ex. este caso."))
        self.assertIn("número cinco", normalize_ptbr("É o nº 5 da lista."))

    def test_numbers_percent_currency_and_units(self):
        self.assertIn("dois mil e vinte e cinco", normalize_ptbr("O relatório é de 2025."))
        self.assertEqual(normalize_ptbr("90% das empresas."), "noventa por cento das empresas.")
        self.assertEqual(normalize_ptbr("R$ 100"), "cem reais")
        self.assertEqual(normalize_ptbr("R$ 1,50"), "um real e cinquenta centavos")
        self.assertEqual(normalize_ptbr("R$ 1.500,00"), "mil e quinhentos reais")
        self.assertEqual(normalize_ptbr("2h de reunião"), "duas horas de reunião")
        self.assertEqual(normalize_ptbr("5 km e 1 kg"), "cinco quilômetros e um quilo")
        self.assertEqual(normalize_ptbr("a 1ª e o 2º"), "a primeira e o segundo")

    def test_acronyms_keep_lowercase_words(self):
        spoken = normalize_ptbr("A IA usa RAG e MCP. Ele ia embora.")
        self.assertIn("i a", spoken)
        self.assertIn("erre a gê", spoken)
        self.assertIn("eme cê pê", spoken)
        self.assertIn("ia embora", spoken)
        self.assertNotIn("IA", spoken)
        self.assertIn("gê pê tê quatro", normalize_ptbr("saiu o GPT-4."))
        self.assertIn("eme pê quatro", normalize_ptbr("sobe o MP4."))

    def test_arrows_from_teleprompter(self):
        spoken = normalize_ptbr("organizar = cada processo → um estagiário")
        self.assertNotIn("→", spoken)
        self.assertNotIn("=", spoken)
        self.assertIn("estagiário", spoken)


if __name__ == "__main__":
    unittest.main()
