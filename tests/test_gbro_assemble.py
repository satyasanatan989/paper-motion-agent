"""
Unit tests for Assemble-from-Empty Staggered Papercraft Mechanics & Color Field Engine.
Inspired by pyang5166/gbro-collage-broll from awesome-claude-video-skills.
"""

import json
import sys
from pathlib import Path
import pytest
import jsonschema
from PIL import Image

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from storyboard.generator import StoryboardGenerator, StoryboardPlan, ScenePlan, CameraSpec, TypographySpec, TransitionSpec
from visual_engine.scene_composer import DynamicSceneComposer
from assets.photographic.generate_photocollage_assets import halftone_cutout, paperize_cutout


def test_schema_validates_gbro_color_field_and_assemble():
    schema_path = _REPO_ROOT / "schemas" / "storyboard_schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    # Valid scene with color_field and assemble_from_empty
    scene = {
        "scene_id": "scene_001",
        "chapter_num": 1,
        "title": "Editorial Halftone Test",
        "duration": 5.0,
        "narration": "Testing assemble-from-empty papercraft mechanics",
        "visual_type": "cinematic_2_5d",
        "environment": "Workshop",
        "camera": {"movement": "slow_dolly_in"},
        "transition": {"type": "directional_wipe"},
        "color_field": "burnt_orange",
        "assemble_from_empty": True,
        "cadence": {
            "fps": 12,
            "boil": True,
            "hold_frames": 2,
            "jitter_px": 1.6,
            "jitter_deg": 0.45,
            "seed": 101
        }
    }

    storyboard_dict = {
        "project_name": "test_gbro",
        "topic": "Assemble-From-Empty Papercraft",
        "language": "hinglish",
        "genre": "science_bio",
        "aspect_ratio": "9:16",
        "resolution": {"width": 1080, "height": 1920},
        "fps": 30,
        "estimated_duration": 15.0,
        "scenes": [
            scene,
            {**scene, "scene_id": "scene_002", "chapter_num": 2, "color_field": "teal_cyan"},
            {**scene, "scene_id": "scene_003", "chapter_num": 3, "color_field": "dark_purple"}
        ]
    }

    jsonschema.validate(instance=storyboard_dict, schema=schema)


def test_storyboard_generator_populates_color_field():
    generator = StoryboardGenerator()
    
    class DummyChapter:
        def __init__(self, num, title):
            self.chapter_num = num
            self.title = title
            self.start_sec = (num - 1) * 5.0
            self.end_sec = num * 5.0
            self.narration_hinglish = f"Chapter {num} narration"
            self.headline_main = f"HEADLINE {num}"
            self.headline_sub = f"CHAPTER {num:02d} · SUB"
            self.keywords = ["TEST", "ASSEMBLY"]

    chapters = [DummyChapter(i, f"Title {i}") for i in range(1, 4)]
    storyboard = generator.generate_storyboard(
        topic="Wheat Grain Digestion",
        chapters=chapters,
        genre="science_bio"
    )

    assert len(storyboard.scenes) == 3
    assert storyboard.scenes[0].color_field == "burnt_orange"
    assert storyboard.scenes[1].color_field == "mustard_yellow"
    assert storyboard.scenes[2].color_field == "teal_cyan"
    assert storyboard.scenes[0].assemble_from_empty is True


def test_scene_composer_generates_gbro_runtime(tmp_path):
    composer = DynamicSceneComposer()
    
    scene = ScenePlan(
        scene_id="scene_001",
        chapter_num=1,
        title="Halftone Collage",
        duration=5.0,
        narration="Testing assemble from empty",
        visual_type="cinematic_2_5d",
        environment="Lab",
        background_tone={"primary": "#1A140E", "secondary": "#2A1F16", "vignette": True},
        camera=CameraSpec(movement="slow_dolly_in"),
        layers=[],
        typography=TypographySpec(badge="CH 01", headline_main="MAIN", headline_sub="SUB", highlight_words=["TEST"]),
        transition=TransitionSpec(type="directional_wipe"),
        color_field="burnt_orange",
        assemble_from_empty=True
    )

    storyboard = StoryboardPlan(
        project_name="gbro_runtime_test",
        topic="Assemble Test",
        language="hinglish",
        genre="science_bio",
        aspect_ratio="9:16",
        resolution={"width": 1080, "height": 1920},
        fps=30,
        estimated_duration=5.0,
        scenes=[scene]
    )

    html_file = composer.compose_stage(storyboard, tmp_path)
    assert html_file.exists()

    html_text = html_file.read_text(encoding="utf-8")
    assert 'filter id="editorial-halftone"' in html_text

    css_text = (tmp_path / "style.css").read_text(encoding="utf-8")
    assert "--cf-burnt-orange" in css_text
    assert ".assemble-piece" in css_text

    js_text = (tmp_path / "timeline.js").read_text(encoding="utf-8")
    assert "colorField" in js_text
    assert "assembleFromEmpty" in js_text
    assert "easeOutBack" in js_text or "c1 = 1.70158" in js_text
    assert "cfMap" in js_text


def test_halftone_cutout_image_processing():
    # Create simple 64x64 RGBA test image with a gradient circle
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    for x in range(64):
        for y in range(64):
            dx, dy = x - 32, y - 32
            if dx*dx + dy*dy <= 24*24:
                # Radial gradient circle
                gray_val = int(255 * (dx*dx + dy*dy) / (24*24))
                img.putpixel((x, y), (gray_val, gray_val, gray_val, 255))

    halftone_result = halftone_cutout(img, dot_size=4, contrast=1.2, paperize=True)
    assert halftone_result is not None
    assert halftone_result.size[0] > 64  # Expanded canvas due to paperize drop shadow
    assert halftone_result.mode == "RGBA"
