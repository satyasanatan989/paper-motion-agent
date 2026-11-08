"""Unit tests for Visual Storyboard Generator and JSON Schema Validation."""

import json
import unittest
from pathlib import Path
import jsonschema

from agent.script_engine import ScriptEngine
from storyboard.generator import StoryboardGenerator

class TestStoryboardGenerator(unittest.TestCase):
    def setUp(self):
        self.script_engine = ScriptEngine()
        self.storyboard_gen = StoryboardGenerator()
        schema_path = Path(__file__).parent.parent / "schemas" / "storyboard_schema.json"
        with open(schema_path, "r", encoding="utf-8") as f:
            self.schema = json.load(f)

    def test_storyboard_generation_and_schema_validation(self):
        topic = "What happens inside your body after eating refined flour?"
        chapters = self.script_engine.generate_script(topic)
        self.assertTrue(len(chapters) >= 5)

        storyboard = self.storyboard_gen.generate_storyboard(
            topic=topic,
            chapters=chapters,
            project_name="test_maida_storyboard",
            genre="health_bio",
            fps=30
        )

        data = storyboard.to_dict()

        # Validate against strict JSON schema
        jsonschema.validate(instance=data, schema=self.schema)

        # Check required structure and content
        self.assertEqual(data["topic"], topic)
        self.assertEqual(len(data["scenes"]), len(chapters))
        for scene in data["scenes"]:
            self.assertIn("scene_id", scene)
            self.assertIn("duration", scene)
            self.assertIn("camera", scene)
            self.assertIn("layers", scene)
            self.assertIn("transition", scene)
            self.assertIn("foley", scene)
            self.assertIn("typography", scene)
            self.assertTrue(len(scene["layers"]) >= 3)
            self.assertIn("movement", scene["camera"])

    def test_scene_timing_and_fps(self):
        chapters = self.script_engine.generate_script("How does a nuclear reactor work?")
        storyboard = self.storyboard_gen.generate_storyboard(
            topic="Nuclear Reactor",
            chapters=chapters,
            fps=60
        )
        data = storyboard.to_dict()
        self.assertEqual(data["fps"], 60)
        total_dur = sum(s["duration"] for s in data["scenes"])
        self.assertAlmostEqual(storyboard.estimated_duration, total_dur, places=2)

if __name__ == '__main__':
    unittest.main()
