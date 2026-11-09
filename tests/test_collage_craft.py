"""
Unit tests for Advanced Editorial Collage Assets & Styling:
- Die-cut Vinyl Stickers with Peel Corner
- Washi Tape with Translucent Fibers & Torn Ends
- Distressed Rubber Stamps with Ink Pooling
- Adaptive Palette Accent Color Sampling
"""

import pytest
import numpy as np
from PIL import Image, ImageDraw

from assets.photographic.generate_photocollage_assets import (
    generate_diecut_sticker,
    generate_washi_tape,
    generate_rubber_stamp,
    sample_accent_color
)


def test_diecut_sticker_generation():
    # Create simple circular test cutout (RGB mode to test conversion)
    src_rgb = Image.new("RGB", (100, 100), (220, 50, 40))
    src = src_rgb.convert("RGBA")
    # Mask out circular alpha
    mask = Image.new("L", (100, 100), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse([10, 10, 90, 90], fill=255)
    src.putalpha(mask)

    # Test top_right peel
    sticker_tr = generate_diecut_sticker(src, border_px=10, peel_corner="top_right", shadow_opacity=0.3)
    assert sticker_tr.mode == "RGBA"
    assert sticker_tr.width > 100
    assert sticker_tr.height > 100

    # Ensure white vinyl border is present
    sticker_arr = np.array(sticker_tr)
    white_mask = (sticker_arr[:, :, 0] > 240) & (sticker_arr[:, :, 1] > 240) & (sticker_arr[:, :, 2] > 240) & (sticker_arr[:, :, 3] > 200)
    assert np.any(white_mask)

    # Test bottom_right peel on RGB input directly
    sticker_br = generate_diecut_sticker(src_rgb, border_px=8, peel_corner="bottom_right", shadow_opacity=0.5)
    assert sticker_br.mode == "RGBA"


def test_washi_tape_generation():
    tape_stripe = generate_washi_tape(width=200, height=45, color=(230, 160, 40), pattern="stripe")
    assert tape_stripe.mode == "RGBA"
    assert tape_stripe.width >= 200
    assert tape_stripe.height >= 45

    # Tape should have semi-transparency
    arr = np.array(tape_stripe)
    alpha = arr[:, :, 3]
    translucent_pixels = (alpha > 50) & (alpha < 240)
    assert np.any(translucent_pixels)

    # Test grid pattern
    tape_grid = generate_washi_tape(width=180, height=40, color=(100, 180, 200), pattern="grid")
    assert tape_grid.mode == "RGBA"


def test_rubber_stamp_generation():
    stamp = generate_rubber_stamp(
        text_outer="TESTED · VERIFIED · ",
        text_center="PASS",
        color=(216, 65, 43),
        diameter=180
    )
    assert stamp.mode == "RGBA"
    assert stamp.width >= 180
    assert stamp.height >= 180

    # Has distinct non-transparent pixels in the stamp color
    arr = np.array(stamp)
    red_ink = (arr[:, :, 0] > 180) & (arr[:, :, 1] < 100) & (arr[:, :, 3] > 100)
    assert np.any(red_ink)


def test_sample_accent_color():
    # Image with vibrant teal and black
    img = Image.new("RGBA", (100, 100), (20, 20, 20, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle([30, 30, 70, 70], fill=(15, 180, 160, 255))

    accent = sample_accent_color(img)
    assert isinstance(accent, tuple)
    assert len(accent) == 3
    # Vibrant teal should be chosen over dark background
    assert accent[1] > accent[0]  # Green > Red
    assert accent[2] > accent[0]  # Blue > Red
