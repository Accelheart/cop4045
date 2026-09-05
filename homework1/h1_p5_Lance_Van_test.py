
import unittest
from h1_p5_Lance_Van import caesar_cipher, caesar_decipher, letter_frequency
class TestCaesarCipher(unittest.TestCase):

    def test_cipher(self):
        self.assertEqual(caesar_cipher("Hello World", 3), "Khoor Zruog")

    def test_decipher(self):
        self.assertEqual(caesar_decipher("Khoor Zruog", 3), "Hello World")

    def test_cipher_preserves_case(self):
        self.assertEqual(caesar_cipher("AbC", 1), "BcD")

    def test_cipher_preserves_spaces(self):
        self.assertEqual(caesar_cipher("abc xyz", 1), "bcd yza")

    def test_letter_frequency(self):
        result = letter_frequency("Hello")

        self.assertEqual(result["h"], 1)
        self.assertEqual(result["e"], 1)
        self.assertEqual(result["l"], 2)
        self.assertEqual(result["o"], 1)

    def test_frequency_ignores_case(self):
        result = letter_frequency("AaA")

        self.assertEqual(result["a"], 3)

    def test_frequency_ignores_non_letters(self):
        result = letter_frequency("a! a? 123")

        self.assertEqual(result["a"], 2)


if __name__ == "__main__":
    unittest.main()