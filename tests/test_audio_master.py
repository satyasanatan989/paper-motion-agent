"""Unit tests for cinematic Audio Master and Foley generator."""

import unittest
import numpy as np
from voice.audio_master import AudioMasterEngine

class TestAudioMaster(unittest.TestCase):
    def setUp(self):
        self.engine = AudioMasterEngine(sample_rate=24000)

    def test_foley_clash(self):
        clash = self.engine.generate_foley_clash(0.2)
        self.assertIsInstance(clash, np.ndarray)
        self.assertEqual(len(clash), int(24000 * 0.2))

    def test_paper_rustle(self):
        rustle = self.engine.generate_paper_rustle(0.3)
        self.assertIsInstance(rustle, np.ndarray)
        self.assertEqual(len(rustle), int(24000 * 0.3))

    def test_cinematic_bgm(self):
        bgm = self.engine.generate_cinematic_bgm(5.0)
        self.assertIsInstance(bgm, np.ndarray)
        self.assertEqual(len(bgm), int(24000 * 5.0))
        self.assertTrue(np.max(np.abs(bgm)) <= 1.0)

    def test_beat_foley_and_track(self):
        pop = self.engine.generate_pop(0.1)
        self.assertIsInstance(pop, np.ndarray)

        stamp = self.engine.generate_stamp_thud(0.2)
        self.assertIsInstance(stamp, np.ndarray)

        tick = self.engine.generate_mechanical_tick(0.05)
        self.assertIsInstance(tick, np.ndarray)

        cues = [
            {"time": 0.2, "sfx": "pop"},
            {"time": 0.5, "sfx": "stamp"},
            {"time": 0.8, "sfx": "tick"},
            {"time": 1.2, "sfx": "paper_flip"}
        ]
        track = self.engine.generate_foley_track(2.0, cues)
        self.assertIsInstance(track, np.ndarray)
        self.assertEqual(len(track), int(24000 * 2.0))

if __name__ == '__main__':
    unittest.main()
