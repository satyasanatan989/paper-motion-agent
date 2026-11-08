"""Unit tests for Food Code visual style system and scientific visual library."""

import unittest
from visual_engine.food_science_library import FoodScienceVisuals, FOOD_CODE_THEME

class TestFoodScienceVisuals(unittest.TestCase):
    def test_brand_color_tokens(self):
        self.assertEqual(FOOD_CODE_THEME["accent_burnt_orange"], "#FF6B00")
        self.assertEqual(FOOD_CODE_THEME["text_warm_white"], "#F5EBE1")
        self.assertIn("#0B0907", FOOD_CODE_THEME["bg_dark"])

    def test_wheat_kernel_macro(self):
        svg = FoodScienceVisuals.wheat_kernel_macro()
        self.assertIn("macro-grain", svg)
        self.assertIn("BRAN", svg)
        self.assertIn("ENDOSPERM", svg)
        self.assertIn("GERM", svg)

    def test_gluten_matrix_macro(self):
        svg = FoodScienceVisuals.gluten_matrix_macro()
        self.assertIn("macro-gluten", svg)
        self.assertIn("pulse-node", svg)
        self.assertIn("GLUTEN-STARCH", svg)

    def test_stomach_acid_reflux_macro(self):
        svg = FoodScienceVisuals.stomach_acid_reflux_macro()
        self.assertIn("gastric-acid", svg)
        self.assertIn("pH 1.5", svg)
        self.assertIn("bubble-float", svg)

    def test_transit_clock_comparison(self):
        svg = FoodScienceVisuals.transit_clock_comparison()
        self.assertIn("transit-clock", svg)
        self.assertIn("24 HOURS", svg)
        self.assertIn("50+ HOURS", svg)

    def test_glucose_ring_molecule(self):
        svg = FoodScienceVisuals.glucose_ring_molecule()
        self.assertIn("molecule-glucose", svg)
        self.assertIn("GLUCOSE", svg)

    def test_food_code_css(self):
        css = FoodScienceVisuals.get_food_code_css()
        self.assertIn("--fc-burnt-orange", css)
        self.assertIn(".brand-badge", css)

if __name__ == '__main__':
    unittest.main()
