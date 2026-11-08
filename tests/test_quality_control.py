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

if __name__ == '__main__':
    unittest.main()
