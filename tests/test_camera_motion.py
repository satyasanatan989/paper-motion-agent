"""Unit tests for 2.5D Physical Camera, Motion Presets & Kinetic Typography."""

import unittest
from visual_engine.camera import CameraController, CameraKeyframe
from visual_engine.motion_presets import MotionEasing, ParticleField
from visual_engine.typography import KineticTypography

class TestCameraMotion(unittest.TestCase):
    def setUp(self):
        self.camera = CameraController()

    def test_camera_movement_bounds(self):
        # Progress 0.0
        k0 = self.camera.get_camera_state("slow_dolly_in", progress=0.0, zoom_start=1.0, zoom_end=1.1)
        self.assertAlmostEqual(k0.zoom, 1.0)
        self.assertAlmostEqual(k0.y, 0.0)

        # Progress 1.0
        k1 = self.camera.get_camera_state("slow_dolly_in", progress=1.0, zoom_start=1.0, zoom_end=1.1)
        self.assertAlmostEqual(k1.zoom, 1.1)
        self.assertAlmostEqual(k1.y, -15.0)
        self.assertAlmostEqual(k1.z, 30.0)

    def test_parallax_layer_transforms(self):
        k = self.camera.get_camera_state("slow_dolly_in", progress=0.8, zoom_start=1.0, zoom_end=1.2)

        bg_css = self.camera.calculate_layer_transform(k, depth_factor=0.2)
        fg_css = self.camera.calculate_layer_transform(k, depth_factor=1.4)

        self.assertIn("translate3d", bg_css)
        self.assertIn("scale", bg_css)
        self.assertIn("translate3d", fg_css)
        self.assertNotEqual(bg_css, fg_css)

    def test_motion_presets_and_particles(self):
        cubic = MotionEasing.ease_out_cubic(0.5)
        self.assertTrue(0.5 < cubic <= 1.0)

        overshoot = MotionEasing.spring_overshoot(1.0)
        self.assertAlmostEqual(overshoot, 1.0)

        svg = ParticleField.generate_particles_svg(field_type="steam", count=10)
        self.assertIn("<circle", svg)
        self.assertIn("r=", svg)

    def test_kinetic_typography_formatting(self):
        badge = KineticTypography.create_chapter_badge(1, "THE SAMOSA TRAP")
        self.assertIn("CHAPTER 01", badge)
        self.assertIn("THE SAMOSA TRAP", badge)

        counter = KineticTypography.create_split_flap_counter("50 HOURS", "TRANSIT TIME")
        self.assertIn("flip-tile", counter)
        self.assertIn(">5<", counter)
        self.assertIn(">0<", counter)

if __name__ == '__main__':
    unittest.main()
