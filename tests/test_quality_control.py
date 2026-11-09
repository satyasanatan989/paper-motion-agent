"""Unit tests for automated post-render Quality Control."""

import unittest
from pathlib import Path
from quality_control.validator import QualityValidator

class TestQualityControl(unittest.TestCase):
    def setUp(self):
        self.validator = QualityValidator()

    def test_mock_video_qc_verification(self):
        # Test nonexistent file handling
        fake_path = Path("output/nonexistent_video.mp4")
        report = self.validator.validate(fake_path, expected_duration=20.0)
        self.assertFalse(report.passed)
        self.assertTrue(len(report.errors) > 0)

    def test_report_dict_serialization(self):
        report = self.validator.validate(Path("output/does_not_exist.mp4"))
        d = report.to_dict()
        self.assertIn("project_name", d)
        self.assertIn("status", d)
        self.assertIn("resolution", d)
        self.assertIn("duration", d)
        self.assertIn("errors", d)
        self.assertIn("warnings", d)

    def test_inspect_storyboard_beats(self):
        from storyboard.generator import StoryboardGenerator, BeatSpec
        beats = [
            BeatSpec(
                beat_id="b01", start=0.0, end=2.5,
                voice="Kya packaged pani healthy hai?",
                headline_top="IS IT HEALTHY?", headline_punch="CHECK FACTS",
                caption_chunk="nariyal pani", caption_highlight="HEALTHY",
                scene_id="tapri", template="notebook_sticker"
            ),
            BeatSpec(
                beat_id="b02", start=2.5, end=5.2,
                voice="Main food technologist hoon sach suniye.",
                headline_top="LAB AUDIT", headline_punch="FOOD CODE",
                caption_chunk="sach suniye", caption_highlight="TRUTH",
                scene_id="desk", template="notebook_sticker"
            )
        ]
        storyboard = StoryboardGenerator().generate_storyboard_from_beats(
            topic="Coconut Water",
            beats=beats,
            project_name="qc_test"
        )
        issues = self.validator.inspect_storyboard(storyboard)
        self.assertEqual(len(issues), 0)

if __name__ == '__main__':
    unittest.main()
