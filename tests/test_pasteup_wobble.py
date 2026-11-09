"""
Unit tests for Pasteup Stop-Motion Wobble & Paper Boil integration.
Inspired by tmoody1973/pasteup from awesome-claude-video-skills.
"""

import json
import sys
from pathlib import Path
import pytest
import jsonschema

# Ensure parent directory is on sys.path for direct script execution
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from storyboard.generator import StoryboardGenerator, StoryboardPlan, ScenePlan, CameraSpec, TypographySpec, TransitionSpec
from visual_engine.scene_composer import DynamicSceneComposer

def test_storyboard_schema_validates_pasteup_cadence():
    schema_path = Path(__file__).resolve().parent.parent / "schemas" / "storyboard_schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    # Valid cadence with pasteup properties
    scene = {
        "scene_id": "scene_001",
        "chapter_num": 1,
        "title": "Stop-Motion Test",
        "duration": 5.0,
        "narration": "Testing pasteup wobble and boil integration",
        "visual_type": "cinematic_2_5d",
        "environment": "Workshop",
        "camera": {"movement": "slow_dolly_in"},
        "transition": {"type": "directional_wipe"},
        "cadence": {
            "fps": 12,
            "boil": True,
            "hold_frames": 2,
            "jitter_px": 1.6,
            "jitter_deg": 0.45,
            "seed": 143
        }
    }

    storyboard_dict = {
        "project_name": "test_pasteup",
        "topic": "Stop-Motion Papercraft",
        "language": "hinglish",
        "aspect_ratio": "9:16",
        "resolution": {"width": 1080, "height": 1920},
        "fps": 30,
        "estimated_duration": 5.0,
        "scenes": [scene, scene, scene]
    }

    # Should validate without throwing jsonschema.ValidationError
    jsonschema.validate(instance=storyboard_dict, schema=schema)

def test_scene_composer_generates_pasteup_runtime_and_css():
    composer = DynamicSceneComposer()

    camera = CameraSpec("slow_dolly_in", True, 1.0, 1.07, "ease")
    trans = TransitionSpec("directional_wipe", 0.45, "center")
    typo = TypographySpec("CH 01", "PASTEUP WOBBLE", "CH 01", ["STOPMOTION"])

    scene = ScenePlan(
        scene_id="scene_001",
        chapter_num=1,
        title="Pasteup Wobble",
        duration=5.0,
        narration="Testing stop motion wobble",
        visual_type="cinematic_2_5d",
        environment="Craft Table",
        background_tone={"primary": "#1A140E", "secondary": "#2A1F16"},
        camera=camera,
        layers=[],
        typography=typo,
        transition=trans,
        foley=[],
        cadence={
            "fps": 12,
            "boil": True,
            "hold_frames": 2,
            "jitter_px": 1.8,
            "jitter_deg": 0.5,
            "seed": 99
        }
    )

    sb = StoryboardPlan(
        project_name="pasteup_test",
        topic="Stop Motion",
        language="hinglish",
        genre="general_explainer",
        aspect_ratio="9:16",
        resolution={"width": 1080, "height": 1920},
        fps=30,
        estimated_duration=5.0,
        soundtrack_preset="health_bio",
        scenes=[scene]
    )

    js = composer._generate_js(sb)
    css = composer._generate_css(sb)

    # Verify JS Pasteup implementation
    assert "computePasteupJitter" in js
    assert "stageJitter" in js
    assert "pasteup pattern" in js.lower()
    assert "cadence.boil" in js
    assert "el.style.translate" in js
    assert "el.style.rotate" in js

    # Verify CSS will-change optimizations for paper boil
    assert "will-change: transform;" in css
    assert "will-change: translate, rotate;" in css
    assert ".visual-stage svg" in css

def test_storyboard_generator_defaults_pasteup_cadence():
    gen = StoryboardGenerator()
    doc_chapters = [
        type("Ch", (), {
            "chapter_num": i,
            "chapter_index": i,
            "title": f"Chapter {i}",
            "narrative_purpose": "hook" if i == 1 else "core_mechanism",
            "primary_fact": f"Fact {i}",
            "supporting_facts": ["Fact A", "Fact B"],
            "suggested_visual": "Visual concept",
            "suggested_metrics": {"METRIC": "100%"},
            "headline_main": f"CH {i}",
            "headline_sub": f"CHAPTER 0{i}",
            "keywords": ["WOBBLE", "BOIL"],
            "start_sec": (i - 1) * 3.0,
            "end_sec": i * 3.0,
            "narration_hinglish": f"Testing pasteup wobble and boil chapter {i}"
        })() for i in range(1, 4)
    ]
    sb = gen.generate_storyboard("test topic", doc_chapters)
    cadence = sb.scenes[0].cadence
    assert cadence is not None
    assert cadence.get("boil") is True
    assert cadence.get("hold_frames") == 2
    assert cadence.get("jitter_px") == 1.6
    assert cadence.get("jitter_deg") == 0.45
    assert "seed" in cadence
