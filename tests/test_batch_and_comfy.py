"""Unit tests for BatchStitcher and ComfyUIAdapter."""

import unittest
from pathlib import Path
from pipeline.batch_stitcher import BatchStitcher
from visual_engine.comfy_adapter import ComfyUIAdapter

class TestBatchAndComfy(unittest.TestCase):
    def test_batch_stitcher_init(self):
        stitcher = BatchStitcher()
        self.assertIsNotNone(stitcher)

    def test_comfy_adapter_offline_graceful(self):
        adapter = ComfyUIAdapter(host="127.0.0.1", port=9999)
        # Port 9999 is closed, should return False without crashing
        self.assertFalse(adapter.is_available())
        self.assertIsNone(adapter.get_hardware_info())

    def test_comfy_sd15_prompt_payload(self):
        adapter = ComfyUIAdapter()
        payload = adapter.build_sd15_food_prompt(
            positive_prompt="steaming bowl of ramen noodles with soft-boiled egg and bok choy",
            width=768,
            height=768,
            seed=1234
        )
        self.assertIn("prompt", payload)
        nodes = payload["prompt"]
        self.assertIn("3", nodes) # KSampler
        self.assertIn("4", nodes) # CheckpointLoader
        self.assertIn("6", nodes) # Positive CLIP
        self.assertIn("ramen noodles", nodes["6"]["inputs"]["text"])

if __name__ == '__main__':
    unittest.main()
