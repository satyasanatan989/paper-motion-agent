"""Unit tests for Hinglish normalizer."""

import unittest
from voice.normalizer import normalize_hinglish_text

class TestNormalizer(unittest.TestCase):
    def test_numbers_conversion(self):
        text = "2200 years ago, Bharat had 100K soldiers."
        norm = normalize_hinglish_text(text)
        self.assertIn("twenty-two hundred", norm)
        self.assertIn("one hundred thousand", norm)

    def test_bce_expansion(self):
        text = "261 BCE war"
        norm = normalize_hinglish_text(text)
        self.assertIn("two sixty-one", norm)
        self.assertIn("B C E", norm)

    def test_symbols(self):
        text = "100K+ soldiers & 24 spokes"
        norm = normalize_hinglish_text(text)
        self.assertIn("plus", norm)
        self.assertIn("and", norm)
        self.assertIn("twenty-four", norm)

if __name__ == '__main__':
    unittest.main()
