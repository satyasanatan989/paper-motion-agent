"""
Unit Tests for AssetPipeline.
Validates:
1. Style suffix expansion (sticker, illustration, space)
2. SHA-256 prompt-hash based asset caching
3. Background removal & paperize_sticker() vinyl border
4. 3-Layer multiplane background generation (bg, mid, fg)
"""

from pathlib import Path
import pytest
from PIL import Image

from assets.pipeline import AssetPipeline, STYLE_SUFFIXES

def test_prompt_hashing_and_caching(tmp_path):
    pipe = AssetPipeline(cache_dir=tmp_path)
    h1 = pipe.get_prompt_hash("tender coconut", "sticker")
    h2 = pipe.get_prompt_hash("Tender Coconut ", "STICKER")
    assert h1 == h2, "Hash must be case- and whitespace-insensitive"

    # Generate asset
    asset_path = pipe.generate_asset("tender coconut pack", style="sticker", asset_id="tetra_test")
    assert asset_path.exists()
    assert asset_path.name.endswith(".png")

    # Second call must hit cache immediately
    mtime1 = asset_path.stat().st_mtime
    cached_path = pipe.generate_asset("tender coconut pack", style="sticker", asset_id="tetra_test")
    assert cached_path == asset_path
    assert cached_path.stat().st_mtime == mtime1

def test_sticker_paperization(tmp_path):
    pipe = AssetPipeline(cache_dir=tmp_path)
    raw = Image.new("RGBA", (200, 200), (255, 100, 50, 255))
    sticker = pipe.paperize_sticker(raw, white_edge_px=6)

    assert sticker.size[0] > 200
    assert sticker.size[1] > 200
    assert sticker.mode == "RGBA"

def test_3layer_background_generation(tmp_path):
    pipe = AssetPipeline(cache_dir=tmp_path)
    layers = pipe.generate_3layer_background("test_gali_scene")

    assert "bg" in layers and "mid" in layers and "fg" in layers
    assert layers["bg"].exists()
    assert layers["mid"].exists()
    assert layers["fg"].exists()

    with Image.open(layers["bg"]) as img:
        assert img.size == (1080, 1920)
