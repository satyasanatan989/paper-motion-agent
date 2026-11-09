"""Unit tests for Food Code visual style system and scientific visual library."""

import unittest
from research.fact_engine import ResearchEngine
from visual_engine.food_science_library import FoodScienceVisuals, FOOD_CODE_THEME
from visual_engine.scene_composer import DynamicSceneComposer
from storyboard.generator import ScenePlan, TypographySpec, CameraSpec, TransitionSpec

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

    def test_ice_cream_vs_frozen_dessert_research(self):
        engine = ResearchEngine()
        doc = engine.research_topic("difference between frozen dessert and an ice cream")
        self.assertEqual(doc.domain, "biology_health")
        self.assertEqual(len(doc.chapters), 6)
        self.assertIn("Cold Deception", doc.chapters[0].title)
        self.assertIn("10% Dairy Law", doc.chapters[1].title)
        self.assertIn("Palm Oil", doc.chapters[2].title)
        self.assertIn("Melting Test", doc.chapters[4].title)

    def test_ice_cream_scene_composer_not_overwritten(self):
        composer = DynamicSceneComposer()
        camera = CameraSpec("slow_zoom_in", True, 1.0, 1.05, "ease")
        trans = TransitionSpec("directional_wipe", 0.4, "center")
        typo = TypographySpec("CH 02", "10% DAIRY LAW", "CH 02", ["MILK"])
        
        scene_ch2 = ScenePlan(
            scene_id="scene_002",
            chapter_num=2,
            title="The 10% Dairy Law",
            duration=16.0,
            narration="Test",
            visual_type="biological_macro",
            environment="Lab",
            background_tone={"primary": "#000", "secondary": "#111"},
            camera=camera,
            layers=[],
            typography=typo,
            transition=trans,
            foley=[]
        )
        html = composer._build_visual_stage_html(scene_ch2)
        self.assertIn("10% MILK FAT", html)
        self.assertNotIn("FIBROUS BRAN", html)

        # Test Chapter 4: 3X Profit Equation
        scene_ch4 = ScenePlan(
            scene_id="scene_004",
            chapter_num=4,
            title="The 3X Profit Equation",
            duration=16.0,
            narration="Test",
            visual_type="biological_macro",
            environment="Lab",
            background_tone={"primary": "#000", "secondary": "#111"},
            camera=camera,
            layers=[],
            typography=typo,
            transition=trans,
            foley=[]
        )
        html_ch4 = composer._build_visual_stage_html(scene_ch4)
        self.assertIn("Rs 450/KG", html_ch4)
        self.assertNotIn("acid-pool-wave", html_ch4)

    def test_food_code_css(self):
        css = FoodScienceVisuals.get_food_code_css()
        self.assertIn("--fc-burnt-orange", css)
        self.assertIn(".brand-badge", css)

if __name__ == '__main__':
    unittest.main()
