"""Unit tests for procedural paper cutouts."""

import unittest
from motion.cutouts import CutoutLibrary

class TestCutouts(unittest.TestCase):
    def test_ashoka_chakra_geometry(self):
        svg = CutoutLibrary.ashoka_chakra(cx=310, cy=310, r=270)
        self.assertIn("s5-chakra", svg)
        self.assertEqual(svg.count("<line"), 24)

    def test_sword_clash(self):
        svg = CutoutLibrary.sword_clash("s2")
        self.assertIn("s2-sword-l", svg)
        self.assertIn("s2-sword-r", svg)
        self.assertIn("s2-sparks", svg)

if __name__ == '__main__':
    unittest.main()
